#!/usr/bin/env python3
"""Maakt de kaartbeelden voor de vaste motieven, in een vaste stijl.

Waarom dit een script is en geen handwerk in een fotobewerker: de motiefkaart is
een lastig slot. sections/categories.liquid toont het beeld via assets/base.css,
regel 231-238, en dat doet drie dingen die je niet ziet aankomen als je losse
foto's beoordeelt:

    .cat      aspect-ratio:4/5, background:var(--bd-navy)
    .cat img  object-fit:cover, opacity:.55
    .cat__body inset:0, padding:2rem, justify-content:flex-end

Het beeld komt dus voor 45% onder navy te liggen, er wordt niets weggesneden, en
de kaart tekent titel, label, omschrijving en knop er onderaan als HTML
overheen. Drie foto's die los prima zijn, worden zo drie kaarten die niet bij
elkaar horen -- en bij een licht kledingstuk wordt de tekst onleesbaar.

Vijf regels vangen dat op. Ze staan uitgeschreven in docs/motieven/README.md, en
scripts/check-motiefbeeld.py meet of ze gehaald worden.

Een motief erbij:
    1. docs/motieven/bron/<sleutel>.jpg neerzetten
    2. hieronder een regel aan MOTIEVEN toevoegen
    3. python3 scripts/motiefbeeld-maken.py
    4. de uitkomst in Shopify bij de kaart zetten

Vereist: Pillow  (pip install Pillow)
"""
import os
import sys

try:
    from PIL import Image, ImageEnhance, ImageStat
except ImportError:
    sys.exit("Pillow ontbreekt. Installeer het met: pip install Pillow")

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(HIER, "docs", "motieven")
BRONMAP = os.path.join(MAP, "bron")

# ---------------------------------------------------------------- de vijf regels

# 1. Formaat. Twee keer de 800px die de kaart opvraagt, dus scherp op retina.
BREEDTE, HOOGTE = 1600, 2000

# 2. Compositie. De onderste 38% is van de tekst; het motief hoort in de rest.
#    FOCUS_DOEL is waar het middelpunt van het motief in het kader belandt.
TEKSTVLAK = 0.38
MOTIEFVLAK = 0.62
FOCUS_DOEL = 0.34
ZOOM_BODEM = 0.65          # zover mag de uitsnede inzoomen om dat te halen
MIN_UITSNEDE = 1200        # smaller dan dit en het opschalen gaat zichtbaar kosten

# 3. Toon. Alles wordt naar dezelfde helderheid getrokken, met iets minder
#    verzadiging en een lichte warme zweem -- navy komt er toch overheen.
DOEL_HELDERHEID = 0.52
HELDERHEID_GRENZEN = (0.6, 1.8)
VERZADIGING = 0.92
WARMTE = 0.06
CREME = (250, 247, 240)

# 4. Leesbaarheid. Een navy verloop in de onderste helft, zodanig dat witte
#    tekst overal in het tekstvlak boven 4,5:1 blijft -- ook bovenin dat vlak,
#    waar het label staat. Een verloop dat pas onderaan vol is, is te laat: het
#    label zit op ongeveer 62% van de hoogte, niet op 95%.
NAVY = (15, 30, 61)
KAARTDEKKING = 0.55        # opacity:.55 uit base.css
VERLOOP_TOP = 0.50
VERLOOP = ((0.50, 0.00), (0.62, 0.55), (1.00, 0.88))

# 5. Terughoudendheid: geen tekst, geen logo, geen kader in het beeld. De kaart
#    tekent dat zelf. Daarom staat er hieronder ook geen enkele tekenroutine.

# ---------------------------------------------------------------- de motieven

# sleutel = de waarde achter `motief:` in de producttag, en tegelijk de
# bestandsnaam. Zie templates/product.vast-motief.json.
# focus = waar het motief in het BRONBEELD zit, als fractie van breedte en
# hoogte. Laat weg als het motief ongeveer midden-boven staat.
MOTIEVEN = [
    {"sleutel": "amsterdam-city-map", "naam": "Amsterdam City Map"},
    {"sleutel": "amsterdam-canal-belt", "naam": "Amsterdam Canal Belt"},
    {"sleutel": "andreaskruizen", "naam": "Andreaskruizen"},
]

STANDAARD_FOCUS = (0.5, 0.42)


# ---------------------------------------------------------------- rekenwerk


def _lineair(kanaal):
    """sRGB-kanaal (0..1) naar lineair licht, zoals de WCAG het voorschrijft."""
    return kanaal / 12.92 if kanaal <= 0.03928 else ((kanaal + 0.055) / 1.055) ** 2.4


def luminantie(rgb):
    r, g, b = (_lineair(k / 255) for k in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_wit_op(rgb):
    """Contrastverhouding van wit tegen een kleur. 4,5:1 is de WCAG-ondergrens
    voor lopende tekst, 3:1 voor grote koppen."""
    return 1.05 / (luminantie(rgb) + 0.05)


def op_de_kaart(rgb):
    """Wat de kaart van deze beeldkleur maakt: opacity:.55 boven navy.

    Dit is de reden dat het beeld niet op zichzelf beoordeeld kan worden. Een
    kleur die in het bestand ruim contrast geeft, kan hier onder de grens
    zakken."""
    return tuple(KAARTDEKKING * rgb[i] + (1 - KAARTDEKKING) * NAVY[i] for i in range(3))


def _verloop_alpha(t):
    """De dekking van het navy verloop op hoogte t (0 boven, 1 onder)."""
    punten = VERLOOP
    if t <= punten[0][0]:
        return 0.0
    for (t0, a0), (t1, a1) in zip(punten, punten[1:]):
        if t <= t1:
            return a0 + (a1 - a0) * (t - t0) / (t1 - t0)
    return punten[-1][1]


def _helderheid(afbeelding):
    """Gewogen gemiddelde over de sRGB-waarden. Bewust niet de lineaire
    luminantie: ImageEnhance.Brightness schaalt sRGB-waarden, dus meten we in
    dezelfde ruimte waarin we bijstellen."""
    r, g, b = ImageStat.Stat(afbeelding.resize((80, 100), Image.LANCZOS)).mean[:3]
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


def _uitsnede(afbeelding, focus):
    """Het 4:5-venster dat het motief op FOCUS_DOEL van de hoogte zet.

    Een 4:5-uitsnede uit een vierkante bron pakt de volle hoogte, en dan valt er
    verticaal niets te schuiven. Om het motief toch omhoog te krijgen mag het
    venster kleiner worden dan het maximum -- inzoomen dus, tot ZOOM_BODEM. Lukt
    het daarbinnen niet, dan komt het motief zo hoog mogelijk te staan en volgt
    er een melding; stil een onbruikbaar beeld afleveren is erger dan geen beeld.
    """
    meldingen = []
    bw, bh = afbeelding.size
    fx, fy = focus
    fy_px = fy * bh

    verhouding = BREEDTE / HOOGTE
    h_max = min(bh, bw / verhouding)
    h_plaatsing = min(fy_px / FOCUS_DOEL, (bh - fy_px) / (1 - FOCUS_DOEL))
    h = max(min(h_max, h_plaatsing), h_max * ZOOM_BODEM)
    h = min(h, h_max)
    w = h * verhouding

    top = max(0.0, min(fy_px - FOCUS_DOEL * h, bh - h))
    links = max(0.0, min(fx * bw - w / 2, bw - w))

    werkelijk = (fy_px - top) / h
    if werkelijk > MOTIEFVLAK:
        meldingen.append(
            f"het motief komt op {werkelijk:.0%} van de hoogte en valt daarmee buiten "
            f"het bovenvlak van {MOTIEFVLAK:.0%}; lever een bron aan waar het motief "
            f"hoger staat, of zet focus= scherper"
        )
    if w < MIN_UITSNEDE:
        meldingen.append(
            f"de uitsnede is {w:.0f}px breed en wordt opgeschaald naar {BREEDTE}px; "
            f"dat kost scherpte - lever zo mogelijk een grotere bron aan"
        )

    return (round(links), round(top), round(links + w), round(top + h)), meldingen


def _toon(afbeelding):
    """Verzadiging en warmte eerst, helderheid daarna.

    In die volgorde, omdat de helderheidscorrectie op de gemeten waarde stuurt:
    meet je vóór de warme zweem, dan verschuift die zweem je meting alsnog."""
    afbeelding = ImageEnhance.Color(afbeelding).enhance(VERZADIGING)
    warm = Image.new("RGB", afbeelding.size, CREME)
    afbeelding = Image.blend(afbeelding, warm, WARMTE)

    gemeten = _helderheid(afbeelding)
    factor = DOEL_HELDERHEID / gemeten if gemeten > 0 else 1.0
    factor = max(HELDERHEID_GRENZEN[0], min(factor, HELDERHEID_GRENZEN[1]))
    return ImageEnhance.Brightness(afbeelding).enhance(factor)


def _verloop(afbeelding):
    """Het navy verloop in de onderste helft inbakken."""
    kolom = Image.new("L", (1, HOOGTE))
    for y in range(HOOGTE):
        kolom.putpixel((0, y), round(255 * _verloop_alpha(y / (HOOGTE - 1))))
    masker = kolom.resize((BREEDTE, HOOGTE), Image.NEAREST)
    laag = Image.new("RGB", (BREEDTE, HOOGTE), NAVY)
    return Image.composite(laag, afbeelding, masker)


def verwerk(afbeelding, focus=STANDAARD_FOCUS, meld=False):
    """Een bronbeeld door de vijf regels halen.

    Geeft de afbeelding terug, of (afbeelding, meldingen) als meld=True."""
    afbeelding = afbeelding.convert("RGB")
    kader, meldingen = _uitsnede(afbeelding, focus)
    uit = afbeelding.crop(kader).resize((BREEDTE, HOOGTE), Image.LANCZOS)
    uit = _verloop(_toon(uit))
    return (uit, meldingen) if meld else uit


def plaatshouder(naam):
    """Het beeld voor een motief dat nog geen bron heeft.

    Bewust zonder tekst: de kaart tekent de naam er zelf al overheen, en een
    tweede naam in het beeld zou daar bovenop komen. De schuine banen maken hem
    herkenbaar onaf zonder dat hij lelijk is -- dat is beter dan een lege kaart,
    en veel beter dan een beeld van een ander motief lenen."""
    # Het masker op kwartformaat tekenen en daarna opschalen: schuine banen
    # blijven schuine banen, en het scheelt drie miljoen putpixel-aanroepen.
    schaal = 4
    bm, hm = BREEDTE // schaal, HOOGTE // schaal
    masker = Image.new("L", (bm, hm), 0)
    breed = 46 // schaal
    for y in range(hm):
        for x in range(bm):
            if ((x + y) // breed) % 2 == 0:
                masker.putpixel((x, y), 255)
    masker = masker.resize((BREEDTE, HOOGTE), Image.NEAREST)

    beeld = Image.new("RGB", (BREEDTE, HOOGTE), (27, 44, 77))
    donker = Image.new("RGB", (BREEDTE, HOOGTE), (22, 37, 63))
    return _verloop(Image.composite(donker, beeld, masker))


# ---------------------------------------------------------------- draaien


def main():
    if not os.path.isdir(BRONMAP):
        os.makedirs(BRONMAP, exist_ok=True)

    gemaakt, plaatsgehouden, gewaarschuwd = 0, 0, 0
    for motief in MOTIEVEN:
        sleutel, naam = motief["sleutel"], motief["naam"]
        doel = os.path.join(MAP, f"{sleutel}.jpg")

        bron = None
        for ext in ("jpg", "jpeg", "png", "webp"):
            kandidaat = os.path.join(BRONMAP, f"{sleutel}.{ext}")
            if os.path.exists(kandidaat):
                bron = kandidaat
                break

        if bron is None:
            plaatshouder(naam).save(doel, "JPEG", quality=88, optimize=True)
            print(f"  ~ {sleutel:<24} plaatshouder (geen bron in docs/motieven/bron/)")
            plaatsgehouden += 1
            continue

        with Image.open(bron) as beeld:
            uit, meldingen = verwerk(
                beeld, focus=motief.get("focus", STANDAARD_FOCUS), meld=True
            )
        uit.save(doel, "JPEG", quality=88, optimize=True)
        print(f"  ✓ {sleutel:<24} uit {os.path.basename(bron)}")
        for m in meldingen:
            print(f"      ! {m}")
            gewaarschuwd += 1
        gemaakt += 1

    print()
    print(
        f"{gemaakt} beeld(en) gemaakt, {plaatsgehouden} plaatshouder(s), "
        f"{gewaarschuwd} waarschuwing(en) -> docs/motieven/"
    )


if __name__ == "__main__":
    main()
