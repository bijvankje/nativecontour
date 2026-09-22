# Themacode van de Amsterdam-lijn

Dit is **geen werkend thema**. Het zijn de bestanden die in het Bordurodam-thema alleen de
Amsterdam-lijn bedienden, zoals ze daar op 22 september 2026 stonden. Ze zijn daar weggehaald
omdat de vier Amsterdam-artikelen uit die winkel gaan; hier staan ze klaar voor het moment dat
deze winkel een eigen thema krijgt.

| Bestand | Wat het doet |
|---|---|
| `templates/collection.amsterdam.json` | De landingspagina: een hero, de motievenrij en een afsluitende band |
| `templates/product.fixed-embroidery-amsterdam.json` | Productpagina met een vast motief, zoals de eerste winkelfase hem had |
| `templates/product.vast-motief.json` | De nieuwere vorm: het motief zit in het product (tag `motief:<sleutel>`), niet in een eigen sjabloon per motief |
| `sections/main-product-fixed-embroidery.liquid` | De sectie onder het eerste sjabloon |
| `sections/categories.liquid` | De motievenrij: kaarten met beeld, titel en link |
| `sections/categories.css` | De opmaak van die kaarten, uitgeknipt uit `assets/base.css` van dat thema |
| `tests/test-motievenrij.js` | Bewaakt dat een kaart zonder link geen dode knop wordt |
| `tests/test-motiefnamen.js` | Bewaakt dat de motiefnamen in beide sjablonen gelijk blijven; de sleutel is de tag op het product |

## Wat er níet bij zit

De sectie die de productpagina van een vaste borduring tekent,
`sections/main-product-vaste-borduring.liquid`, is in het Bordurodam-thema gebleven: de tassen
daar draaien erop. Die sectie kan met motief-blokken overweg — dat is precies wat
`product.vast-motief.json` hierboven aanvoert — dus wie dit hier weer aan de praat wil krijgen,
heeft die sectie erbij nodig. Ze staat in `bijvankje/bordurodam`.

Verder ontbreken `layout/theme.liquid`, de rest van `assets/base.css`, de header en de footer:
alles wat niet specifiek van de Amsterdam-lijn was.

## De twee tests

Ze draaiden mee in `scripts/check-theme.sh` van het andere thema en verwachten de paden zoals ze
dáár lagen (`sections/…`, `templates/…`, en `liquidjs` uit `node_modules`). Zet je hier een thema
neer, pas dan eerst de paden bovenin de twee bestanden aan.
