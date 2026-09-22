# Waar deze skills vandaan komen

Niet met de hand bijgehouden. Dit is een kopie, neergezet door
`scripts/skills-bijwerken.sh`. Bijwerken doe je door dat script te draaien,
niet door hier te typen. Zie [docs/claude-skills.md](../../docs/claude-skills.md)
voor waarom ze in de repo staan en niet in een marketplace.

Alles in deze map is geleend. Krijgt nativecontour een eigen skill, zet zijn
mapnaam dan in `eigen=()` bovenin het script, anders veegt de volgende
bijwerkronde hem weg.

| Map | Herkomst | Licentie | Commit |
|---|---|---|---|
| superpowers (14 skills) | [obra/superpowers](https://github.com/obra/superpowers) | MIT | `5bf4e78` |
| ui-ux-pro-max (7 skills) | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | `dcc40ff` |
| remotion (12 skills) | [remotion-dev/claude-code-plugin](https://github.com/remotion-dev/claude-code-plugin) | MIT | `b66b588` |
| caveman (1 skill) | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | MIT | `ae26f3a` |

Bijgewerkt op 2026-09-21.

`caveman` is de uitzondering: alleen de map `skills/caveman/` uit dat project is
overgenomen, niet de rest. De bovenstroomse repo is verder een heel
software-project (proxyserver, Go-binaries, browserextensie, telemetrie) om die
ene modus te leveren als plugin met hooks; hier is het gewoon een SKILL.md, net
als de andere drie.

Twee dingen die het script aanpast aan de originelen, en waarom:

- `design/` heet hier `ui-ux-design/`. Claude heeft zelf al een skill die
  `design` heet (het ontwerpcanvas) en gelijke namen botsen.
- Paden die met `~/.claude/skills/` beginnen zijn `.claude/skills/` geworden.
  De originelen gaan ervan uit dat ze per gebruiker geinstalleerd staan; hier
  staan ze in de repo.

## Wat er niet bij zit

Elke winkel-specifieke skill blijft in zijn eigen repo. StudioMadeau heeft
`nieuw-artikel` (L-Shop-Team-import voor babytextiel) en Bordurodam heeft
`borduurprogrammas` (Wilcom-worksheets van RT Designers) — beide geschreven op
de werkwijze en de bestanden van die ene winkel, dus geen van beide is
meegekomen hierheen. Zodra nativecontour zelf zo'n winkel-specifieke skill
nodig heeft (bijvoorbeeld voor het aanleveren van vaste motieven), hoort daar
een eigen versie voor te komen — geen kopie die stiekem naar een andere repo
verwijst.
