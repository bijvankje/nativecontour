# De Amsterdam-lijn

Dit is het materiaal van de Amsterdam-lijn: geborduurde souvenirs en cadeaus met een
Amsterdams motief, voor particulieren. Het lag tot 22 september 2026 in de repo
[`bijvankje/bordurodam`](https://github.com/bijvankje/bordurodam) en hoort daar niet thuis —
Bordurodam is de zakelijke winkel (bedrijfskleding borduren met een eigen logo), de
Amsterdam-lijn is een eigen winkel met eigen klanten. Daarom staat het hier.

## Wat er is meegekomen

| Bestand | Wat het is |
|---|---|
| [`docs/motieven/`](./motieven/) | De kaartbeelden van de drie motieven (grachtengordel, stadsplattegrond, andreaskruizen), met de regels waaraan zo'n beeld moet voldoen |
| [`scripts/motiefbeeld-maken.py`](../scripts/motiefbeeld-maken.py) | Maakt van een bronfoto een kaartbeeld dat aan die regels voldoet |
| [`scripts/check-motiefbeeld.py`](../scripts/check-motiefbeeld.py) | Meet of de beelden de regels halen; draaien met `python3 scripts/check-motiefbeeld.py` |
| [`docs/voorstellen/motiefkaarten.html`](./voorstellen/motiefkaarten.html) | De afweging achter de motiefkaarten, als beeld in de browser |
| [`docs/superpowers/specs/2026-09-11-amsterdam-particulier-design.md`](./superpowers/specs/2026-09-11-amsterdam-particulier-design.md) | Het ontwerp voor de particuliere kant: hoe een bezoeker een motief kiest |
| [`docs/backups/bordurodam-amsterdam-2026-08-28.zip`](./backups/) | Een complete export van het Shopify-thema `bordurodam-amsterdam`, 28 augustus 2026. Te uploaden onder *Online Store → Themes → Add theme → Upload zip file*; het komt binnen als niet-gepubliceerd thema |

De twee scripts en de map `docs/` raken geen winkel: Shopify leest alleen de mappen die
samen een thema vormen. Er komt hier dus niets vanzelf ergens live te staan.

## Wat nog in de bordurodam-repo staat

De **themacode** van de Amsterdam-lijn is bewust achtergebleven, omdat de winkel
bordurodam.nl die op dit moment nog gebruikt: de collectie *Amsterdam* heeft daar vier
producten en een eigen pagina. Het gaat om:

- `templates/collection.amsterdam.json` — de landingspagina
- `templates/product.fixed-embroidery-amsterdam.json` en `sections/main-product-fixed-embroidery.liquid` — de productpagina met een vast motief
- `sections/categories.liquid` — de motievenrij op die pagina

Die verhuizen pas als de Amsterdam-producten uit de winkel van Bordurodam gaan. Dat is een
aparte beslissing: hij verandert wat bezoekers zien.

Hetzelfde geldt voor het Shopify-thema `bordurodam-amsterdam` zelf. Dat staat nog in de
winkel van Bordurodam, niet gepubliceerd, en is daar tot nu toe bewaard omdat het de enige
plek is waar de instellingen en de homepage van die eerste fase nog compleet staan. De zip
hierboven is daar een kopie van, dus zodra deze winkel zijn eigen thema heeft, kan het thema
daar weg.

## De referenties in de meegekomen teksten

De teksten in `docs/motieven/README.md` en de spec verwijzen naar bestanden uit het
Bordurodam-thema (`sections/categories.liquid`, `assets/base.css`, `templates/`). Die
bestanden staan hier niet. Ze blijven bruikbaar als beschrijving van hoe de motiefkaart zich
gedraagt — het beeld ligt voor 45% onder een donkere laag, de tekst staat onderin — maar de
paden kloppen pas als dit thema er is.
