#!/usr/bin/env python3
"""Bewaakt de beloftes die scripts/motiefbeeld-maken.py doet.

De motiefkaart op de Amsterdam-pagina is geen gewoon beeldslot. base.css:231-238
legt het beeld op `opacity:.55` boven navy en tekent titel, label, omschrijving
en knop er als HTML overheen, onderaan. Twee dingen zijn daardoor geen smaak
maar een eis:

  1. In het tekstvlak moet witte tekst contrast halen, hoe licht het bronbeeld
     ook is. Een wit kledingstuk daar geeft zonder ingrijpen wit-op-#8C929D --
     3,1:1, ruim onder de 4,5:1 die de WCAG voor lopende tekst vraagt.
  2. De beelden moeten onderling als een set lezen, anders zijn drie kaarten
     naast elkaar rommeliger dan drie kaarten zonder beeld.

Beide zijn hier meetbaar gemaakt, want beide zijn stil kapot te maken: een
verloop dat een paar procent te vroeg uitdooft ziet er op zichzelf prima uit en
breekt pas op de kaart, en dan alleen bij lichte foto's.

Draaien:  python3 scripts/check-motiefbeeld.py
Vereist:  Pillow  (pip install Pillow)
"""
import importlib.util
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))

try:
    from PIL import Image, ImageStat
except ImportError:
    print("overgeslagen - Pillow ontbreekt (pip install Pillow)")
    sys.exit(0)

# Het script heeft koppeltekens in zijn naam, zoals de rest van scripts/. Dat is
# geen geldige modulenaam, dus laden we het via zijn pad.
_spec = importlib.util.spec_from_file_location(
    "motiefbeeld", os.path.join(HIER, "motiefbeeld-maken.py")
)
mbm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mbm)


fouten = []


def eis(voorwaarde, omschrijving):
    if voorwaarde:
        print(f"  ✓ {omschrijving}")
    else:
        print(f"  ✗ {omschrijving}")
        fouten.append(omschrijving)


def helderheid(rgb):
    """Gewogen gemiddelde over de sRGB-waarden. Niet de WCAG-luminantie -- dit
    is de maat waar de toonregeling op stuurt, en die rekent in sRGB."""
    r, g, b = rgb
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


def klein(afbeelding):
    """Meten op een verkleinde kopie. Scheelt miljoenen pixels per controle en
    verandert niets aan rijgemiddelden, waar het hier over gaat."""
    return afbeelding.resize((160, 200), Image.LANCZOS).convert("RGB")


def rijen(afbeelding, van, tot, stappen=24):
    """Per horizontale strook: (gemiddelde kleur, spreiding binnen de strook).

    De spreiding is er om het motief te vinden. De donkerste strook zoeken werkt
    niet: het verloop onderin is per definitie het donkerst. Een motief maakt
    juist verschil bínnen een rij, en een verloop niet.
    """
    k = klein(afbeelding)
    h = k.height
    uit = []
    for i in range(stappen):
        y0 = int(h * (van + (tot - van) * i / stappen))
        y1 = max(y0 + 1, int(h * (van + (tot - van) * (i + 1) / stappen)))
        strook = k.crop((0, y0, k.width, y1))
        gem = tuple(ImageStat.Stat(strook).mean[:3])
        spreiding = ImageStat.Stat(strook.convert("L")).stddev[0]
        uit.append((gem, spreiding))
    return uit


def bron(kleur, formaat=(1400, 1750), vlek=None, onderband=None):
    """Een effen bronbeeld. `vlek` zet er een donkere schijf in op een fractie
    van de hoogte -- dat is het motief waar de uitsnede op mikt. `onderband`
    maakt de onderste helft wit: een licht kledingstuk dat het tekstvlak vult."""
    img = Image.new("RGB", formaat, kleur)
    w, h = formaat
    if onderband is not None:
        for y in range(int(h * onderband), h):
            for x in range(w):
                img.putpixel((x, y), (255, 255, 255))
    if vlek is not None:
        straal = int(min(w, h) * 0.12)
        cx, cy = w // 2, int(h * vlek)
        for y in range(max(0, cy - straal), min(h, cy + straal)):
            for x in range(max(0, cx - straal), min(w, cx + straal)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= straal**2:
                    img.putpixel((x, y), (20, 20, 20))
    return img


print("1. Het formaat ligt vast")
uit = mbm.verwerk(bron((160, 150, 140)))
eis(
    (uit.width, uit.height) == (mbm.BREEDTE, mbm.HOOGTE),
    f"{mbm.BREEDTE} x {mbm.HOOGTE}, ongeacht het formaat van de bron",
)
eis(
    mbm.verwerk(bron((160, 150, 140), formaat=(900, 900))).size == (mbm.BREEDTE, mbm.HOOGTE),
    "ook een vierkante bron komt er als 4:5 uit",
)

print("2. Witte tekst haalt contrast in het hele tekstvlak")
# Het scherpste geval dat een sfeerbeeld oplevert: een donkere bovenkant met een
# wit kledingstuk dat het tekstvlak vult. Juist die combinatie glipt langs de
# toonregeling -- het gemiddelde van het beeld klopt, en toch is het onderste
# vlak wit. Niet het gemiddelde beeld, wel het beeld dat de kaart breekt.
zwaar = mbm.verwerk(bron((70, 74, 82), onderband=0.5))
laagste = min(
    mbm.contrast_wit_op(mbm.op_de_kaart(kleur))
    for kleur, _ in rijen(zwaar, 1 - mbm.TEKSTVLAK, 1.0)
)
eis(
    laagste >= 4.5,
    f"licht kledingstuk in het tekstvlak: laagste contrast {laagste:.1f}:1",
)
egaal_wit = mbm.verwerk(bron((255, 255, 255)))
laagste_wit = min(
    mbm.contrast_wit_op(mbm.op_de_kaart(kleur))
    for kleur, _ in rijen(egaal_wit, 1 - mbm.TEKSTVLAK, 1.0)
)
eis(
    laagste_wit >= 4.5,
    f"een volledig wit bronbeeld: laagste contrast {laagste_wit:.1f}:1",
)

print("3. De toon trekt verschillende bronnen naar elkaar toe")


def toon(afbeelding):
    """Helderheid van het bovenvlak. Boven het verloop meten, anders meet je het
    verloop en niet de toonregeling."""
    kl = rijen(afbeelding, 0.0, mbm.VERLOOP_TOP)
    n = len(kl)
    return helderheid(tuple(sum(k[0][c] for k in kl) / n for c in range(3)))


h_donker = toon(mbm.verwerk(bron((92, 96, 104))))
h_licht = toon(mbm.verwerk(bron((178, 172, 162))))
eis(
    abs(h_donker - h_licht) <= 0.06,
    f"twee bronnen die 0,33 uit elkaar lagen liggen nu {abs(h_donker - h_licht):.2f} uit elkaar",
)
eis(
    max(abs(h_donker - mbm.DOEL_HELDERHEID), abs(h_licht - mbm.DOEL_HELDERHEID)) <= 0.08,
    f"beide komen bij het doel {mbm.DOEL_HELDERHEID:.2f} uit "
    f"({h_donker:.2f} en {h_licht:.2f})",
)

print("4. Het motief wordt naar het bovenvlak geschoven")
# Een bron met het motief op 62% van de hoogte: precies op de grens waar de
# tekst begint. De uitsnede hoort hem omhoog te halen.
uit = mbm.verwerk(bron((170, 165, 158), vlek=0.62), focus=(0.5, 0.62))
metingen = rijen(uit, 0.0, 1.0, stappen=40)
motief_y = max(range(len(metingen)), key=lambda i: metingen[i][1]) / len(metingen)
eis(
    motief_y < mbm.MOTIEFVLAK,
    f"het motief staat op {motief_y:.0%} van de hoogte, binnen het bovenvlak "
    f"van {mbm.MOTIEFVLAK:.0%}",
)

print("5. Een onhaalbare uitsnede wordt gemeld en niet stilgezwegen")
# Staat het motief zo laag dat het er alleen met extreme inzoom in past, dan
# moet het script dat zeggen. Stil een onbruikbaar beeld afleveren is erger dan
# geen beeld: niemand kijkt de uitvoer na als er geen waarschuwing bij staat.
_, meldingen = mbm.verwerk(bron((170, 165, 158)), focus=(0.5, 0.92), meld=True)
eis(any("bovenvlak" in m for m in meldingen), "een motief op 92% levert een waarschuwing op")
_, meldingen = mbm.verwerk(bron((170, 165, 158), formaat=(600, 750)), meld=True)
eis(
    any("scherpte" in m for m in meldingen),
    "een te kleine bron levert een waarschuwing over scherpte op",
)
_, meldingen = mbm.verwerk(bron((170, 165, 158), vlek=0.42), focus=(0.5, 0.42), meld=True)
eis(not meldingen, "een bron die gewoon past levert geen ruis op")

print("6. De plaatshouder gedraagt zich als een gewoon motiefbeeld")
ph = mbm.plaatshouder("Amsterdam Canal Belt")
eis((ph.width, ph.height) == (mbm.BREEDTE, mbm.HOOGTE), "zelfde formaat als de rest")
laagste = min(
    mbm.contrast_wit_op(mbm.op_de_kaart(kleur))
    for kleur, _ in rijen(ph, 1 - mbm.TEKSTVLAK, 1.0)
)
eis(laagste >= 4.5, f"ook hier haalt de kaarttekst contrast ({laagste:.1f}:1)")

print()
if fouten:
    print(f"FAIL - {len(fouten)} controle(s) niet gehaald")
    sys.exit(1)
print("PASS - de motiefbeelden voldoen aan de kaart")
