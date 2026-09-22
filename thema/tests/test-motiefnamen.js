/* De drie motieven van de Amsterdam-lijn heten in het Nederlands, en de twee
   sjablonen die ze noemen moeten het over dezelfde drie eens zijn.

   Waarom dit een toets is en niet alleen een afspraak:

   - De naam uit product.vast-motief.json komt via properties[Borduurmotief] op
     de bestelling terecht. De titel uit collection.amsterdam.json staat op het
     kaartje waar de klant op klikt. Lopen die twee uiteen, dan bestelt iemand
     iets anders dan hij aanklikte.
   - De sleutel is de tag die de eigenaar in Shopify-admin op het product zet
     (motief:<sleutel>). Verandert de sleutel hier zonder dat de tag meegaat, dan
     vindt de sectie het motief niet meer en valt de pagina terug op "kies zelf".
     Daarom staan de sleutels hier met naam en toenaam.

   Besloten in het ontwerp van de Amsterdam-lijn, dat sinds 22 september 2026 in de
   repo nativecontour staat (docs/superpowers/specs/2026-09-11-amsterdam-particulier-design.md):
   Nederlands voor de hele tak.

   Draaien:  node scripts/test-motiefnamen.js
*/
const fs = require('fs');
const path = require('path');

const WORTEL = path.join(__dirname, '..');

/* Shopify zet boven een sjabloon dat het zelf schreef een /* ... *\/-kop. Die is
   geldig voor Shopify maar niet voor JSON.parse. */
const leesSjabloon = (naam) => JSON.parse(
  fs.readFileSync(path.join(WORTEL, 'templates', naam), 'utf8').replace(/\/\*[\s\S]*?\*\//, '')
);

const VERWACHT = [
  { sleutel: 'stadsplattegrond', naam: 'Stadsplattegrond' },
  { sleutel: 'grachtengordel', naam: 'Grachtengordel' },
  { sleutel: 'andreaskruizen', naam: 'Andreaskruizen' },
];

const fouten = [];
const eis = (voorwaarde, wat) => { if (!voorwaarde) fouten.push(wat); };

// 1. De productpagina: drie motiefblokken, met de besloten sleutels en namen.
const product = leesSjabloon('product.vast-motief.json');
const motiefBlokken = Object.values(product.sections)
  .flatMap((s) => Object.values(s.blocks || {}))
  .filter((b) => b.type === 'motief');

eis(motiefBlokken.length === 3, `product.vast-motief.json heeft ${motiefBlokken.length} motiefblokken in plaats van 3`);

VERWACHT.forEach(({ sleutel, naam }) => {
  const blok = motiefBlokken.find((b) => b.settings.sleutel === sleutel);
  eis(blok !== undefined, `product.vast-motief.json kent geen motief met sleutel "${sleutel}"`);
  if (blok) {
    eis(blok.settings.naam === naam,
        `het motief "${sleutel}" heet "${blok.settings.naam}" in plaats van "${naam}"`);
  }
});

// 2. De landingspagina noemt dezelfde drie, in dezelfde volgorde.
const collectie = leesSjabloon('collection.amsterdam.json');
const kaartSectie = Object.values(collectie.sections).find((s) => s.type === 'categories');
eis(kaartSectie !== undefined, 'collection.amsterdam.json heeft geen categories-sectie met de motieven');

if (kaartSectie) {
  const titels = (kaartSectie.block_order || Object.keys(kaartSectie.blocks))
    .map((id) => kaartSectie.blocks[id].settings.title);
  eis(JSON.stringify(titels) === JSON.stringify(VERWACHT.map((m) => m.naam)),
      `de kaarttitels zijn ${JSON.stringify(titels)} in plaats van ${JSON.stringify(VERWACHT.map((m) => m.naam))}`);

  /* De blok-id draagt de sleutel, zodat je aan de id ziet welke tag erbij hoort.
     Shopify laat de id's staan zoals ze in het sjabloon stonden. */
  VERWACHT.forEach(({ sleutel }) => {
    eis(Object.keys(kaartSectie.blocks).includes('motief-' + sleutel),
        `collection.amsterdam.json heeft geen blok "motief-${sleutel}"`);
  });
}

// 3. Geen Engelse resten in de twee sjablonen, en niet het afgekapte "Andreas".
['product.vast-motief.json', 'collection.amsterdam.json'].forEach((naam) => {
  const ruw = fs.readFileSync(path.join(WORTEL, 'templates', naam), 'utf8');
  ['Amsterdam City Map', 'amsterdam-city-map', 'Amsterdam Canal Belt', 'amsterdam-canal-belt']
    .forEach((rest) => eis(!ruw.includes(rest), `${naam} noemt nog "${rest}"`));
  eis(!/"(naam|title)":\s*"Andreas"/.test(ruw), `${naam} gebruikt nog de afgekapte naam "Andreas"`);
});

// 4. De hint in de sectie geeft een Nederlands voorbeeld, niet een Engels.
const sectie = fs.readFileSync(path.join(WORTEL, 'sections/main-product-vaste-borduring.liquid'), 'utf8');
const hint = /"id":\s*"sleutel"[^}]*"info":\s*"([^"]*)"/.exec(sectie);
eis(hint !== null, 'de sleutel-instelling in main-product-vaste-borduring.liquid heeft geen info-hint meer');
if (hint) {
  eis(!hint[1].includes('amsterdam-city-map'),
      'de hint bij de sleutel geeft nog het Engelse amsterdam-city-map als voorbeeld');
}

if (fouten.length) {
  console.error('  ✗ motiefnamen:');
  fouten.forEach((f) => console.error('    - ' + f));
  process.exit(1);
}
console.log(`  ✓ motiefnamen: ${VERWACHT.length} motieven Nederlands, sjablonen eens over naam en sleutel`);
