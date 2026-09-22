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

De **themacode** kwam op dezelfde dag alsnog mee, zodra vaststond dat de vier
Amsterdam-artikelen uit die winkel gaan. Ze staat in [`thema/`](../thema/), met een eigen
leesmij erbij: de landingspagina, de twee productsjablonen met een vast motief, de sectie
eronder, de motievenrij met haar opmaak en de twee tests.

Eén stuk bleef daar bewust achter: `sections/main-product-vaste-borduring.liquid`, de sectie
die een productpagina met een vaste borduring tekent. De tassen van Bordurodam draaien erop.
Die sectie kan ook met motief-blokken overweg, dus wie `product.vast-motief.json` hier weer
wil gebruiken, heeft haar erbij nodig.

In de winkel van Bordurodam moeten de vier artikelen en de collectie *Amsterdam* nog met de
hand weg; dat staat op de admin-lijst van die repo. Het Shopify-thema `bordurodam-amsterdam`
blijft daar voorlopig staan: het is de enige plek waar de instellingen en de homepage van de
eerste fase compleet zijn. De zip hierboven is een export daarvan, en een export bevat niet
alles — dus weg mag het thema pas als deze winkel op eigen benen staat.

## De referenties in de meegekomen teksten

De teksten in `docs/motieven/README.md` en de spec verwijzen naar bestanden uit het
Bordurodam-thema (`sections/categories.liquid`, `assets/base.css`, `templates/`). Die
bestanden staan hier niet. Ze blijven bruikbaar als beschrijving van hoe de motiefkaart zich
gedraagt — het beeld ligt voor 45% onder een donkere laag, de tekst staat onderin — maar de
paden kloppen pas als dit thema er is.
