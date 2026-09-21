# nativecontour

Derde webshop, naast `bijvankje/studiomadeau` en `bijvankje/bordurodam`. Nog in opzet —
dit bestand groeit mee met wat besloten wordt, het is geen vastgelegd plan vooraf.

## Wat al vaststaat (21 september 2026)

- **Doelgroep:** particulieren, net als StudioMadeau — geen bedrijven.
- **Product:** alleen **vaste borduringen** (vaste motieven), geen personalisatie met naam
  of tekst. Dat is het stuk van Bordurodam (vaste motieven, eigen logo) toegepast op een
  particuliere klant in plaats van een zakelijke.
- **Domein:** een URL die er al is — welke, en of die al gekoppeld is, staat hieronder bij
  de open punten.
- **Shopify:** eigen abonnement, eigen winkel. Niet onder StudioMadeau's winkel gehangen —
  reden: één winkel = één checkout = één prijsweergave, en een vierde variant (vaste
  motieven + btw-incl + geen staffel) naast StudioMadeau's tekst-producten in dezelfde
  winkel vergroot het risico op precies het soort btw-fout dat bij StudioMadeau al twee
  keer is misgegaan. Budget is geen belemmering.
- **Repo:** eigen repo, zelfde reden als de StudioMadeau/Bordurodam-splitsing — sessies en
  chats voor deze winkel gescheiden houden van de andere twee, en straks een eigen set
  regels zonder if/else tussen winkels.

## Hoe dit zich verhoudt tot de andere twee repo's

| | `bijvankje/studiomadeau` | `bijvankje/bordurodam` | `bijvankje/nativecontour` (hier) |
|---|---|---|---|
| Koper | particulier | zakelijk | particulier |
| Waarmee | naam en tekst | eigen logo | vaste motieven |
| Prijzen | incl. btw | excl. btw | incl. btw (wettelijk verplicht bij consumenten, ACM) |
| Staffelkorting | nee | 5% vanaf 25, 10% vanaf 50 | nog te besluiten — bij particulier ligt "nee" voor de hand, net als StudioMadeau |

Deze drie repo's delen infrastructuur (thema-opbouw, controlescript, skills) niet met elkaar
via een gedeeld pakket — dat is bewust nog niet gedaan, zie "Nog te doen" hieronder.

## Nog open

- Domeinnaam/URL vastleggen en de status ervan (al gekoppeld aan een Shopify-winkel of nog
  niet).
- Shopify-winkel zelf: nog aanmaken.
- Welke vaste motieven, en of die (deels) overkomen uit de Bordurodam-catalogus of nieuw
  zijn.
- Staffelkorting: wel of niet.
- Thema-basis: forken van StudioMadeau (zoals StudioMadeau ooit van Bordurodam is
  afgesplitst) of vanaf een schone Shopify-theme beginnen.
- De vier bewakingslagen die de andere twee repo's hebben (controlescript, pre-push-hook,
  CI-workflow, sessie-hook "stand van zaken") — hier nog niet opgezet; volgt zodra er
  code/thema is om te bewaken.

## Logboek

Nog geen `docs/logboek/` — die zet ik op zodra er onderwerpen zijn om vast te leggen, naar
hetzelfde patroon als de andere twee repo's (een bestand per onderwerp, niet per sessie).
