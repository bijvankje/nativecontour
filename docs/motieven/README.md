# Motiefbeelden

De kaartbeelden voor de vaste motieven op de Amsterdam-pagina, en de manier waarop ze
gemaakt worden. Gemaakt op 8 september 2026, omdat er van de drie motieven één een
screenshot had en twee niets — en omdat er nog meer motieven aankomen.

Shopify leest deze map niet; net als de rest van `docs/` valt hij buiten de mappen die het
thema vormen. De bestanden hier gaan met de hand naar *Content → Files*.

De afweging staat visueel in [`../voorstellen/motiefkaarten.html`](../voorstellen/motiefkaarten.html).

## Waarom een script en geen fotobewerker

De motiefkaart is een lastig slot. `sections/categories.liquid` toont het beeld via
`assets/base.css`, regel 231-238:

```css
.cat       { aspect-ratio:4/5; background:var(--bd-navy) }
.cat img   { object-fit:cover; opacity:.55 }
.cat__body { inset:0; padding:2rem; justify-content:flex-end }
```

Drie gevolgen die je niet ziet aankomen als je losse foto's beoordeelt:

1. **Het beeld komt voor 45% onder navy te liggen.** Kleuren dempen, contrast zakt, en een
   druk beeld wordt modder.
2. **Er wordt niets weggesneden.** `cover` op een 4:5-beeld in een 4:5-vak toont alles,
   randen incluis.
3. **De kaart tekent er tekst overheen**, onderaan. Label, titel, omschrijving en knop.

Daardoor is "mooie foto" niet het criterium. Drie foto's die los prima zijn, worden zo drie
kaarten die niet bij elkaar horen — en bij een licht kledingstuk wordt de tekst
onleesbaar. Dat laatste is geen smaakkwestie: een witte hoodie in het tekstvlak geeft
wit-op-`#8C929D`, oftewel **3,1:1**, terwijl de WCAG **4,5:1** vraagt voor lopende tekst.

## De vijf regels

`scripts/motiefbeeld-maken.py` legt ze op. Ze zijn de stijl; verander je er één, dan
verandert de hele set — en dat is precies de bedoeling, want dan draai je het script
opnieuw en lopen de oude motieven mee.

| | Regel | Waarom |
|---|---|---|
| **1** | **1600 × 2000** | Twee keer de 800px die de kaart opvraagt, dus scherp op retina. `image_url: width: 800` schaalt zelf terug. |
| **2** | **Motief in de bovenste 62%** | De onderste 38% is van de tekst. Staat het motief in de bron lager, dan snijdt het script strakker om het omhoog te halen — tot een grens, daarna waarschuwt hij. |
| **3** | **Toon naar één doel** | Zelfde helderheid (0,52), verzadiging × 0,92, en 6% crème erdoorheen. Drie verschillende bronnen gaan als één reeks lezen. |
| **4** | **Navy verloop onderin** | Van 50% hoogte naar beneden oplopend tot 88% dekking. Niet pas onderaan vol: het label staat op ongeveer 62% van de hoogte, niet op 95%. |
| **5** | **Niets in het beeld** | Geen tekst, geen logo, geen kader. De kaart tekent dat zelf; dubbel zou botsen. |

Regel 4 is de enige die met een getal te bewijzen valt, en dat is precies waarom hij
gemeten wordt. `scripts/check-motiefbeeld.py` voert een bronbeeld met een wit kledingstuk
in het tekstvlak door de molen en meet elke rij: de laagste uitkomst is **9,7:1**, ruim
boven de 4,5:1. Een verloop dat een paar procent te vroeg uitdooft ziet er op zichzelf
prima uit en breekt pas op de kaart — vandaar de controle.

## Een motief erbij

```bash
# 1. het aangeleverde beeld neerzetten (jpg, jpeg, png of webp)
cp ~/Downloads/Gemini_Generated_Image_xxxx.png docs/motieven/bron/amsterdam-canal-belt.png

# 2. een regel toevoegen aan MOTIEVEN bovenin scripts/motiefbeeld-maken.py
#    {"sleutel": "amsterdam-canal-belt", "naam": "Amsterdam Canal Belt"},

# 3. draaien -- verwerkt alle motieven opnieuw, dus de set blijft gelijk
python3 scripts/motiefbeeld-maken.py

# 4. controleren
python3 scripts/check-motiefbeeld.py
```

Daarna `docs/motieven/<sleutel>.jpg` uploaden in *Content → Files* en bij de kaart zetten
in het themabeheer.

**De sleutel is niet vrij te kiezen.** Het is de waarde achter `motief:` in de producttag,
en die staat in `templates/product.vast-motief.json`. Zo weten het beeld, het blok en het
product van elkaar dat ze over hetzelfde motief gaan.

**Staat het motief niet midden-boven in de bron?** Zet er dan
`"focus": (0.5, 0.62)` bij — breedte en hoogte als fractie, gemeten in het bronbeeld. Het
script mikt dat punt op 34% van de kaarthoogte.

**Nog geen bron?** Dan maakt het script een plaatshouder: navy met schuine banen, zichtbaar
onaf. Bewust zonder tekst, want de kaart zet de naam er zelf al overheen. Dat is beter dan
een lege kaart, en veel beter dan een beeld van een ander motief lenen — een klant die op
Canal Belt klikt en de stadsplattegrond ziet, wordt op het verkeerde been gezet.

**Pillow nodig:** `pip install Pillow`. Zonder Pillow slaat de controle zichzelf over in
plaats van te struikelen, net als de node-stappen in `check-theme.sh`.

## De bron: een prompt voor Gemini

De bestaande sfeerbeelden zijn zo gemaakt — zeven voor de Stadsplattegrond, drie voor de
Andreaskruizen, alle in `Content → Files` te vinden door op `Gemini` te zoeken. Voor Canal
Belt bestaat er nog niets.

Hieronder de prompt om er nieuwe bij te maken die in dezelfde reeks passen. **Laat alles
staan behalve de vier regels tussen accolades** — juist het gelijk houden van licht,
kadering en afwerking maakt er een set van.

```text
A vertical 4:5 portrait photograph of a person wearing a {KLEDINGSTUK} in {KLEUR}.

Centred on the chest is a machine-embroidered design: {MOTIEF}. The embroidery is
worked in a single thread colour ({GAREN}), about 20 cm wide, with visible
satin-stitch texture: individual thread passes catching the light, sitting very
slightly raised above the fabric weave, edges crisp where the stitching stops.
No print and no transfer -- it must read unmistakably as stitching in thread.

Framing: the chest and the embroidery sit in the upper two thirds of the frame.
The lower third is calm and uncluttered -- plain fabric or softly blurred
background -- with nothing in it that asks to be read.

Setting: {LOCATIE}, softly out of focus behind the subject.
Light: overcast Dutch daylight, soft and directional from the left, no harsh
highlights on the fabric, no direct sun.
Look: natural colours, gently muted, a hint of warmth. Shot on a 50 mm lens at
f/2.8, fine film grain, documentary rather than catalogue.

No text, no lettering, no logos other than the described embroidery, no
watermarks, no borders, no hands covering the chest.
```

Per motief in te vullen:

| | Amsterdam City Map | Amsterdam Canal Belt | Andreaskruizen |
|---|---|---|---|
| `{MOTIEF}` | a fine-line street map of the Amsterdam city centre, the canal rings and radiating streets as thin even stitched lines inside a rectangular block | the Amsterdam canal belt: four concentric curved canals from the Singel to the Prinsengracht with their connecting cross-streets, as an arc of fine stitched lines | the three Saint Andrew's crosses from the Amsterdam coat of arms, stacked vertically, as three bold solid stitched X shapes |
| `{KLEDINGSTUK}` | crew-neck sweatshirt | hooded sweatshirt | hooded sweatshirt |
| `{KLEUR}` | deep navy | off-white | sage green |
| `{GAREN}` | pale grey-blue | deep navy | deep navy |
| `{LOCATIE}` | a canal house window in Amsterdam | a bridge over an Amsterdam canal | a brick side street in Amsterdam |

Drie dingen die in de praktijk het verschil maken:

- **Vraag er meer dan één.** Vier of vijf per motief, en kies daarna. Kadering is waar het
  meestal misgaat: het motief zakt te laag, of iemand houdt een hand voor de borst.
- **Zo groot mogelijk.** Het script schaalt naar 1600px breed en waarschuwt als de uitsnede
  smaller dan 1200px uitkomt. Een bron van 1024×1024 haalt dat net niet.
- **Kijk of het als borduurwerk leest.** Beeldmodellen maken van borduurwerk graag een
  gladde print. Is er geen steekstructuur te zien, gooi hem dan weg — het is een
  borduurbedrijf, en dat is precies het detail waar een klant op let.

### Eén waarschuwing die hierbij hoort

Een gegenereerd beeld toont **een aannemelijk motief, niet het motief dat jullie
borduren.** Zeker bij de plattegrond en de grachtengordel: het model tekent iets wat op een
kaart van Amsterdam lijkt, en dat is niet hetzelfde ontwerp als het borduurprogramma dat de
klant geleverd krijgt.

Voor een kaartachtergrond op 55% dekking onder navy is dat prima — dat is sfeer. Voor de
**productgalerij** is het dat niet: daar koopt iemand op wat hij ziet. Zorg dus dat er van
elk motief minstens één echte foto of scan van de werkelijke borduring in de
productgalerij staat, en houd het gegenereerde beeld bij de sfeer.

## Wat er nu ligt

| Motief | Bron | Uitkomst |
|---|---|---|
| `amsterdam-city-map` | — | plaatshouder |
| `amsterdam-canal-belt` | — | plaatshouder |
| `andreaskruizen` | — | plaatshouder |

Alle drie nog plaatshouders: de echte sfeerbeelden staan in Shopify en zijn vanuit de
werkomgeving niet op te halen (`cdn.shopify.com` is er geblokkeerd). Zodra de bronbeelden
in `bron/` staan en het script draait, verandert deze tabel mee.
