# De Amsterdam-lijn naar particulieren

Ontwerp van 11 september 2026. Aanleiding: de vraag hoe we verder kunnen met de
Amsterdam-lijn nu die zich op particulieren richt, terwijl de winkel sinds 7 september
uitsluitend zakelijk is ingericht.

Dit is de afweging plus de volgorde. Wat er gebouwd wordt staat hieronder; wat er in de
admin moet gebeuren staat er apart, want dat ligt bij de eigenaar.

## De kern in één alinea

De winkel wordt **één winkel voor zakelijk én particulier**. De prijs staat standaard
**inclusief btw** met een schakelaar naar exclusief die onthouden wordt, de bedrijfsnaam bij
het afrekenen wordt optioneel, en de voorwaarden krijgen een consumentendeel. De omslag
gebeurt **niet nu**: de winkel gaat eerst zakelijk live en de particuliere ronde ligt op een
branch tot de Amsterdam-lijn echt te koop staat. Op de dag zelf is het één handeling, want
een half omgezette winkel spreekt zichzelf tegen.

## Wat er al klaarligt

De techniek voor de motieven is af, gebouwd op 31 augustus 2026 en beschreven in
[assortiment-vaste-borduring.md](../../assortiment-vaste-borduring.md):

- `templates/product.vast-motief.json` met de motiefmodus in
  `sections/main-product-vaste-borduring.liquid` — motief per blok (sleutel, naam,
  afbeelding, prijs, plaats, formaat, positie van de proefopstelling), het product wijst er
  één aan met de tag `motief:<sleutel>`.
- Eén vaste prijs per borduring, ingevuld door de winkel. Geen schatting, geen steekaantal,
  geen offertegrens van 18 cm, geen opstartkosten.
- Garenkleur als verplichte keuze op de pagina, meegestuurd als eigenschap.
- De proefopstelling zet het motief op de bestaande kledingfoto's, dus er hoeft per
  kledingstuk niets nieuws gefotografeerd te worden.
- De btw-schakelaar bestaat als instelling: `settings.show_price_incl` en
  `settings.price_footnote` in `config/settings_schema.json`.

## Wat particulier blokkeert, en waarom het meer is dan de btw-regel

Vier dingen, waarvan het eerste het zwaarste weegt en nergens op een lijst stond.

**1. De checkout weigert een particulier.** *Settings → Checkout → Customer information →
Company name* staat sinds 9 september op **Required**. Een consument kan niet afrekenen.
Die instelling geldt voor de hele winkel en is niet per tak te zetten.

**2. Prijzen exclusief btw mogen alleen bij een uitsluitend zakelijke winkel**, en de winkel
zegt dat nu op drie plekken: de voetregel, de voorwaarden en de checkout. Zodra één
Amsterdam-hoodie aan een consument verkocht kan worden, moeten die drie alle drie mee.

**3. De huidige schakelaar toont inclusief als bijregel.** `settings.show_price_incl` maakt er
`€ 26,16 excl. btw · € 31,65 incl. btw` van. Voor consumenten hoort het inclusief-bedrag het
leidende bedrag te zijn, niet de voetnoot. Aanzetten is dus niet genoeg.

**4. Het herroepingsrecht keert terug voor deze lijn.** De winkel leunt nu op artikel 6:230p
BW: kleding met het logo van de klant is maatwerk en gaat niet retour. Een kant-en-klare
hoodie met **ons eigen** motief uit een catalogus is dat veel minder vanzelfsprekend — reken
op veertien dagen bedenktijd, met retouren die wél doorverkoopbaar zijn. Dat raakt geen code
maar wel het retourbeleid en de voorraad.

> Punt 4 is geen juridisch advies. Het is een signalering die door iemand met verstand van
> consumentenrecht bevestigd moet worden voordat de lijn open gaat.

**Waarom er geen tussenweg is.** Het idee om de logo-tak zakelijk te houden en alleen de
motief-tak particulier te maken loopt stuk op punt 1: de checkout is winkelbreed. Wie kan
afrekenen kan beide takken kopen, dus een consument komt hoe dan ook op een logo-pagina
terecht. Per tak een andere prijsweergave is daarmee juridisch het zwakste van de drie paden
en is afgevallen.

## Besloten op 11 september 2026

| Vraag | Besluit |
|---|---|
| Eén winkel of gescheiden? | **Eén winkel**, zakelijk én particulier. Geen tweede Shopify-winkel. |
| Wanneer? | **Eerst zakelijk live**, de particuliere omslag als tweede ronde op een branch. |
| Prijsweergave? | **Schakelaar incl./excl., standaard incl.**, de keuze wordt onthouden. |
| Taal van de motiefnamen? | **Nederlands**, voor de hele lijn. |

## De namen

Nederlands voor de hele tak. De drie motieven heten:

| Was | Wordt | Tag |
|---|---|---|
| Amsterdam City Map | **Stadsplattegrond** | `motief:stadsplattegrond` |
| Amsterdam Canal Belt | **Grachtengordel** | `motief:grachtengordel` |
| Andreas | **Andreaskruizen** | `motief:andreaskruizen` |

"Andreas" was geen motiefnaam maar een afgekapte, en las als een voornaam. "Andreas Crosses"
bestaat niet als naam voor de drie kruizen uit het stadswapen.

De tags staan nog nergens vast, dus dit is het goedkoopste moment om ze Nederlands te maken:
later kost een tag-wijziging ook de automatische collectie die eraan hangt.

**Het motief staat vooraan in de producttitel**, alleen in deze tak: `Stadsplattegrond
hoodie` in plaats van `Tee Jays Hooded Sweatshirt Amsterdam City Map`. In het Assortiment
blijft de leveranciersnaam vooraan staan. Twee takken, twee naamlogica's, omdat er twee
soorten kopers zijn. Een producttitel wijzigen raakt de handle niet, dus de bestaande
concept-producten kunnen hernoemd worden zonder omleiding.

## Wat er gebouwd wordt: de schakelaar

### Waar hij staat

Rechts in de servicebalk, in `site-topbar__right` in `sections/header.liquid`, naast het
telefoonnummer. Dat is de enige plek die op elke pagina staat en niet met de prijs meescrollt.

### Hoe hij werkt

**Elke prijsregel rendert beide bedragen in de HTML; één class op `<html>` bepaalt welk
bedrag zichtbaar is.** Dat moet zo, en dat is de enige echte ontwerpbeslissing hier: Shopify
cachet pagina's volledig, dus een keuze per bezoeker kan niet uit Liquid komen. De keuze
staat in `localStorage` en wordt vóór de eerste paint gezet door een klein inline script in
`layout/theme.liquid` — anders ziet de bezoeker het bedrag omspringen.

Standaard staat de winkel op **inclusief btw**. Een zakelijke bezoeker klikt één keer en
ziet daarna overal exclusief, inclusief de winkelmand.

De checkout blijft altijd inclusief: Shopify staat op *Include sales tax in product price* en
dat blijft zo. Dat is ook wat de btw-notitie in
[borduurprijzen.md](../../logboek/borduurprijzen.md) adviseerde — de winkel omzetten naar
prijzen exclusief btw zou juist deze ronde onmogelijk maken.

### Welke bestanden

| Bestand | Wat erin verandert |
|---|---|
| `sections/header.liquid` | de schakelaar in de servicebalk |
| `layout/theme.liquid` | inline script dat de class zet vóór de eerste paint |
| `assets/vat-toggle.js` | **nieuw** — omzetten, onthouden, de class bijwerken |
| `snippets/product-card.liquid` | beide bedragen renderen in plaats van één |
| `sections/main-product.liquid` | idem, op de logopagina |
| `sections/main-product-vaste-borduring.liquid` | idem, op de motief- en vaste-borduringpagina |
| `sections/main-product-namen.liquid` | idem — zie hieronder |
| de winkelmand | toont al beide bedragen; alleen de leidende moet meebewegen |
| `config/settings_schema.json` | `show_price_incl` wordt een driestand |
| `scripts/check-theme.sh` | een stap erbij |

`settings.show_price_incl` wordt een driestand in plaats van een vinkje: **uit** (zoals nu,
één bedrag excl.), **altijd beide**, **schakelaar**. Daarmee blijft `main` de winkel die hij
vandaag is totdat de stand bewust omgezet wordt, en is de omslag één instelling in plaats van
een merge.

De stap in `check-theme.sh` eist dat elke plek die een prijs toont beide bedragen rendert.
Zonder die bewaking valt er bij een volgende wijziging stilletjes één uit, en dan toont de
winkel een consument een bedrag exclusief btw zonder dat iemand het merkt.

### Twee dingen die onderweg boven kwamen

**`sections/main-product-namen.liquid` luistert nergens naar.** Regel 36 toont
`excl. btw · {{ price_incl }} incl. btw` hardgecodeerd, buiten `settings.show_price_incl` om.
Nu onzichtbaar omdat de namenpagina stilligt, maar naamborduring hoort bij dezelfde
consumentgerichte ronde als de motieven, dus hij gaat mee.

**`sections/main-product-fixed-embroidery.liquid` toont helemaal geen btw-regel.** Dat is de
oude Amsterdam-sectie uit fase één, met all-in souvenirprijzen.

## Voorstel: de fase-één-sectie naar `geparkeerd/`

`sections/main-product-fixed-embroidery.liquid` en
`templates/product.fixed-embroidery-amsterdam.json` gaan naar `docs/geparkeerd/`, met de
reden en de terugzetinstructie ernaast zoals de andere bestanden daar.

Waarom: ze zijn vervangen door de motiefmodus, ze rekenen geen borduurgeld, ze kennen de
staffel en de gevouwen winkelmand niet, en het motief zit in het sjabloon in plaats van in
het product. Dat laatste is precies het model dat faalde bij het tweede motief — het
gekopieerde Andreaskruizen-sjabloon in de export van `bordurodam-amsterdam` zegt nog steeds
`design_name: "Amsterdam Stadsplattegrond"`, en zet dus het verkeerde motief op de bestelling.

Dit is een voorstel en geen besluit; de eigenaar beslist of ze blijven staan.

## Wat er in de admin moet gebeuren

Dit deel ligt bij de eigenaar en bepaalt de doorlooptijd. De code wacht er niet op.

### De vier instellingen van de omslag

Deze vier horen bij elkaar en gaan op één dag om:

1. *Settings → Checkout → Customer information → Company name* van **Required** naar
   **Optional**. Zonder dit kan een consument niet afrekenen.
2. De instelling *Prijsweergave* op **schakelaar**, en `price_footnote` leeg of neutraal.
3. *Settings → Legal → Terms of service*: een consumentendeel erbij, met de versieregel mee
   omhoog. De eigen artikelen nakijken op "btw" en "consument" zodat de kop ze niet
   tegenspreekt — dezelfde controle als op 9 september.
4. *Return and refund policy*: het herroepingsrecht van veertien dagen voor de
   catalogusmotieven, met de 6:230p-uitzondering expliciet beperkt tot logowerk.

De bronteksten staan in [teksten/beleid/](../../teksten/beleid/) en worden daar bijgewerkt
voordat ze geplakt worden.

### De Amsterdam-lijn zelf

1. De drie hoodies het sjabloon `vast-motief` geven, elk met zijn tag
   (`motief:stadsplattegrond`, `motief:grachtengordel`, `motief:andreaskruizen`).
2. De producttitels Nederlands maken, met het motief vooraan.
3. Per motief een afbeelding uploaden en in het sjabloon kiezen, met de positie van de
   proefopstelling erbij.
4. De prijs van het product zo zetten dat de borduring erin zit; het prijsveld bij het motief
   blijft leeg, dan zegt de pagina "borduring inbegrepen".
5. De collectie `onze-ontwerpen` aanmaken, de drie erin hangen, **en publiceren naar de
   Online Store**. De bestaande collectie *Amsterdam* staat op **nul verkoopkanalen** en
   geeft dus een 404 — dat is dezelfde val waar de navigatie-ronde al twee keer in liep.
6. De tak *Onze ontwerpen* in *Content → Menu's*, met *Amsterdam* als kolom eronder. Het
   megamenu leest het tweede en derde niveau van hetzelfde menu, dus dit is geen themawerk.
7. Het losse concept-product `Sweater gemeleerd blauw, Grachtengordel Amsterdam` uit fase één
   is niet hetzelfde artikel als de Grachtengordel-hoodie. Eén van de twee moet weg.

Het borduurprogramma van de grachtengordel ontbreekt in `docs/embroidery-programs.csv`, en
dat maakt niet uit: bij eigen motieven stelt de winkel de prijs vast, dus er wordt niets uit
steken afgeleid.

### Let op bij het publiceren

De drie hoodies hebben producttype `Sweaters & Hoodies`. Zodra de categoriecollecties op
producttype draaien liften ze mee in Bovenkleding en staan ze tussen de bedrijfskleding.
Zolang ze op concept staan lost dat zichzelf op, daarna niet meer. Wil je de twee takken
gescheiden houden, dan moet die categorieregel ze uitsluiten — op vendor of op de
`motief:`-tag.

## De volgorde

1. **Nu:** niets aan `main`. De winkel gaat live zoals hij is, zakelijk.
2. **Op een branch:** de schakelaar bouwen, met de bewakingsstap in `check-theme.sh`.
   Te bekijken op een draft theme, die de echte catalogus leest — 331 Clique-producten en
   216 Chaud Devant-artikelen die met één klik omgaan. Dat is de beste test die er is.
3. **Parallel, bij de eigenaar:** de motieffoto's en de drie prijzen. Dat is de echte
   doorlooptijd.
4. **Samen, op één dag:** de vier instellingen om, de branch naar `main`, de collectie
   publiceren, het menu erbij.

De omslag is omkeerbaar tot stap 4, en op stap 4 is hij één handeling.

## Wat hier bewust niet in zit

- **Meerdere borduursoorten per product** (logo én motief én tekst op dezelfde pagina). Op
  31 augustus besloten voorlopig niet te bouwen: dezelfde klant wil zelden allebei.
- **Naamborduring / personaliseren.** Hoort bij dezelfde koper als de motieven en komt
  vermoedelijk in een volgende ronde, maar heeft een eigen prijsvraag (steken volgen uit
  tekens, letterhoogte en lettertype) die een dataklus is en geen indelingsklus.
- **De grachtengordel in de designstore.** Niet nodig: eigen motieven hebben een vaste prijs.
- **Shopify omzetten naar prijzen exclusief btw.** Dat zou de hele klasse btw-fouten laten
  verdwijnen, maar maakt deze ronde onmogelijk.
