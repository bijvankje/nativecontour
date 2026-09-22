/* Rendert sections/categories.liquid -- het kaartenraster dat op de
   landingspagina van Onze ontwerpen de motieven toont -- en controleert wat er
   gebeurt als een kaart geen link heeft.

   Dat is geen bedacht geval. De drie blokken in
   templates/collection.amsterdam.json staan alle drie op "link": "", omdat de
   producten waar ze naar moeten wijzen nog niet bestaan. Een kaart die dan een
   <a href=""> oplevert, is een knop "Bekijk" die de pagina herlaadt: de
   bezoeker klikt en belandt op dezelfde plek.

   Draaien:  npm install liquidjs && node scripts/test-motievenrij.js
*/
const fs = require('fs');
const path = require('path');
const { Liquid } = require('liquidjs');

const WORTEL = path.join(__dirname, '..');
const engine = new Liquid({
  root: [path.join(WORTEL, 'sections'), path.join(WORTEL, 'snippets')],
  extname: '.liquid',
  partials: path.join(WORTEL, 'snippets'),
});
engine.registerFilter('image_url', (img) => (img && img.src) || String(img || ''));

const bron = fs.readFileSync(path.join(WORTEL, 'sections/categories.liquid'), 'utf8');
const sjabloon = bron.replace(/\{%-?\s*schema\s*-?%\}[\s\S]*?\{%-?\s*endschema\s*-?%\}/, '');

const fouten = [];
const eis = (voorwaarde, wat) => { if (!voorwaarde) fouten.push(wat); };

/* De sectie draagt geen eigen <style>, maar de klassenamen staan wel in
   assets/base.css. Hier wordt alleen de gerenderde markup getoetst. */
const markup = (html) => html
  .replace(/<style[\s\S]*?<\/style>/g, '')
  .replace(/<script[\s\S]*?<\/script>/g, '');

const scope = (blokken) => ({
  section: {
    settings: { eyebrow: 'Ons werk', title: 'Vaste motieven', text: 'Kies je motief.' },
    blocks: blokken.map((s) => ({ type: 'cat', settings: s, shopify_attributes: '' })),
  },
});

/* De blokken zoals ze werkelijk in het sjabloon staan. Shopify zet soms een
   /* ... *\/-kop boven een JSON-sjabloon; die moet eraf voor JSON.parse. */
const echteBlokken = () => {
  const ruw = fs.readFileSync(path.join(WORTEL, 'templates/collection.amsterdam.json'), 'utf8')
    .replace(/\/\*[\s\S]*?\*\//, '');
  const t = JSON.parse(ruw);
  const sectie = Object.values(t.sections).find((s) => s.type === 'categories');
  if (!sectie) throw new Error('geen categories-sectie in collection.amsterdam.json');
  return Object.values(sectie.blocks).map((b) => b.settings);
};

(async () => {
  // 1. Een kaart mét link is een link, en belooft de klik met zijn CTA.
  const metLink = markup(await engine.parseAndRender(sjabloon, scope([
    { tag: 'Motief', title: 'Stadsplattegrond', desc: 'De binnenstad.', cta: 'Bekijk', link: '/collections/stadsplattegrond' },
  ])));
  eis(/<a[^>]*class="cat"[^>]*href="\/collections\/stadsplattegrond"/.test(metLink)
      || /<a[^>]*href="\/collections\/stadsplattegrond"[^>]*class="cat"/.test(metLink),
      'een kaart met een link levert geen <a> naar die link op');
  eis(metLink.includes('Bekijk'), 'de CTA-tekst staat niet op een kaart die wel ergens naartoe gaat');
  eis(metLink.includes('Stadsplattegrond'), 'de titel staat niet op de kaart');

  // 2. Een kaart zonder link mag geen href="" opleveren: dat herlaadt de pagina.
  const zonderLink = markup(await engine.parseAndRender(sjabloon, scope([
    { tag: 'Motief', title: 'Grachtengordel', desc: 'Van Singel tot Prinsengracht.', cta: 'Bekijk', link: '' },
  ])));
  eis(!/href=""/.test(zonderLink), 'een kaart zonder link levert href="" op, en dat herlaadt de pagina');
  eis(!/<a[^>]*class="cat"/.test(zonderLink), 'een kaart zonder link is alsnog een <a>, dus klikbaar zonder bestemming');
  eis(!zonderLink.includes('Bekijk'), 'een kaart zonder bestemming belooft toch een klik met zijn CTA');

  // 3. Titel en omschrijving blijven staan; alleen de klik valt weg.
  eis(zonderLink.includes('Grachtengordel'), 'de titel verdwijnt als er geen link is');
  eis(zonderLink.includes('Van Singel tot Prinsengracht.'), 'de omschrijving verdwijnt als er geen link is');

  // 4. Hetzelfde op de blokken die werkelijk in het sjabloon staan.
  const echt = markup(await engine.parseAndRender(sjabloon, scope(echteBlokken())));
  eis(!/href=""/.test(echt), 'de blokken in collection.amsterdam.json leveren dode links op');

  /* 5. De kaartinhoud wordt met capture opgevangen en daarna uitgevoerd. Zou die
        uitvoer ontsnapt worden, dan stond de hele kaart als leesbare tekst op de
        pagina in plaats van als opmaak -- een stille, totale breuk. Getoetst
        tegen een engine met outputEscape: die laat deze drie eisen vallen. */
  const metFoto = markup(await engine.parseAndRender(sjabloon, scope([
    { image: { src: 'foto.png' }, tag: 'Motief', title: 'Stadsplattegrond', desc: 'De binnenstad.', cta: 'Bekijk', link: '/collections/stadsplattegrond' },
  ])));
  eis(metFoto.includes('<div class="cat__body">'), 'de kaartinhoud komt als tekst terug in plaats van als opmaak');
  eis(/<img[^>]+src="foto\.png"/.test(metFoto), 'de foto van een kaart wordt niet gerenderd');
  eis(!/&lt;/.test(metFoto), 'er staat ontsnapte HTML in de uitvoer');

  if (fouten.length) {
    console.error('  ✗ motievenrij:');
    fouten.forEach((f) => console.error('    - ' + f));
    process.exit(1);
  }
  console.log('  ✓ motievenrij: een kaart zonder link is geen dode knop (5 scenario’s)');
})().catch((e) => { console.error('  ✗ motievenrij rendert niet: ' + e.message); process.exit(1); });
