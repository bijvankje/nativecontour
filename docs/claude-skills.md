# Extra skills voor Claude

Vier geleende skill-sets staan in deze repo, zodat Claude ze in elke sessie heeft:
**Superpowers**, **ui-ux-pro-max**, **Remotion** en **Caveman**. Ze raken het thema niet —
Shopify negeert de map `.claude/` volledig — en ze staan los van de winkel: het is
werkwijze, geen inhoud.

Dit is dezelfde opzet als bij `bijvankje/studiomadeau`, overgenomen als eigen kopie: het
script haalt de vier bovenstroomse repo's rechtstreeks op, niet via studiomadeau. Zo blijft
deze repo los van de andere twee, zoals [CLAUDE.md](../CLAUDE.md) vastlegt.

## Waarom niet gewoon `/plugin install`

**In web-sessies werkt dat niet.** Het commando `/plugin` bestaat er niet, en de
marketplaces uit `settings.json` worden er niet opgehaald: een web-sessie start met een
lege plugin-lijst, hoe netjes die instellingen ook staan. Er komt dan nooit één skill uit.

Wat wél altijd werkt is een map onder `.claude/skills/`. Daarom staan alle vier de sets als
kopie in de repo in plaats van als verwijzing.

| Waar je werkt | Krijgt de skills via |
|---|---|
| Web-sessies op deze repo | de map `.claude/skills/` in de repo |
| Claude-app op je eigen computer | dezelfde map, want je hebt de repo gekloond |
| claude.ai-chat en Cowork | niet — dat gaat buiten de repo om |

## Wat er staat

35 skills, alle vier MIT-licentie.

| Set | Herkomst | Skills | Wat het doet |
|---|---|---|---|
| Superpowers | [obra/superpowers](https://github.com/obra/superpowers) | 14 | werkwijze bij programmeren: eerst uitvragen, dan plan, dan bouwen; testen, systematisch debuggen, code review |
| ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 | UI/UX-advies: 192 kleurenpaletten, 74 lettertypecombinaties, contrast en toegankelijkheid |
| Remotion | [remotion-dev/claude-code-plugin](https://github.com/remotion-dev/claude-code-plugin) | 12 | video's maken door ze te programmeren in React |
| Caveman | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 1 | terse, token-zuinige antwoordstijl |

De precieze commits waar deze kopie vandaan komt staan in
[`.claude/skills/HERKOMST.md`](../.claude/skills/HERKOMST.md).

Let op waar ze wel en niet op aansluiten. `ui-ux-pro-max` kent React, Vue en Tailwind maar
geen Shopify Liquid: het advies over kleur, contrast en typografie is bruikbaar, de
voorgestelde code niet — vertaal die zelf naar Liquid. `remotion` heeft een React-project
nodig en kan in dit thema niets doen.

## Wat er niet bij zit

Winkel-specifieke skills komen niet mee. StudioMadeau heeft `nieuw-artikel`
(L-Shop-Team-levering voor babytextiel) en Bordurodam heeft `borduurprogrammas`
(Wilcom-worksheets van RT Designers) — allebei geschreven op de werkwijze en de bestanden
van die ene winkel. Zodra nativecontour zelf zo'n winkel-specifieke skill nodig heeft, hoort
daar een eigen versie voor te komen, niet een kopie die naar een andere repo verwijst — zie
[`.claude/skills/HERKOMST.md`](../.claude/skills/HERKOMST.md).

## Nog niet aangezet

StudioMadeau en Bordurodam zetten deze skills en de vier bewakingslagen (controlescript,
pre-push-hook, CI-workflow, sessie-hook "stand van zaken") aan via hooks in
`.claude/settings.json`. Die hooks staan hier nog niet: [CLAUDE.md](../CLAUDE.md) legt vast
dat de bewakingslagen wachten tot er code/thema is om te bewaken. De skills zijn dus wel
aanwezig, maar Claude wacht tot iets ze oproept in plaats van dat `using-superpowers`
automatisch bij sessiestart wordt voorgelezen.

## Bijwerken

```bash
./scripts/skills-bijwerken.sh
```

Dat haalt de vier bovenstroomse repo's op, zet ze opnieuw neer en schrijft
`.claude/skills/HERKOMST.md` met de commits erbij. Bekijk daarna `git diff` en commit.

Twee dingen past het script aan de originelen aan, en waarom:

- `design/` heet hier `ui-ux-design/`. Claude heeft zelf al een skill die `design` heet en
  gelijke namen botsen.
- Paden die met `~/.claude/skills/` beginnen worden `.claude/skills/`. De originelen gaan
  ervan uit dat ze per gebruiker geïnstalleerd staan; hier staan ze in de repo.
