#!/usr/bin/env bash
#
# Zet de vier plugins uit docs/claude-skills.md als gewone skills in .claude/skills/.
#
# Waarom niet gewoon `/plugin install`: in web-sessies bestaat dat commando niet,
# en de `extraKnownMarketplaces` in .claude/settings.json worden daar niet
# opgehaald -- de sessie start met een lege plugin-lijst. Skills die als map in
# de repo staan worden wél altijd geladen. Daarom staan ze hier in de repo in
# plaats van in een marketplace.
#
# Draaien om bij te werken naar de nieuwste versie van alle vier:
#
#     ./scripts/skills-bijwerken.sh
#
# Daarna `git diff` bekijken en committen. Het script schrijft ook
# .claude/skills/HERKOMST.md met de commits waar deze kopie vandaan komt.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
doel="$repo_root/.claude/skills"
werk="$(mktemp -d)"
trap 'rm -rf "$werk"' EXIT

# Eigen skills van deze repo blijven staan; alleen de geleende gaan eruit.
# Zodra nativecontour er zelf een krijgt, zet je zijn mapnaam hier bij.
eigen=()

echo "Ophalen..."
git clone --depth 1 --quiet https://github.com/obra/superpowers.git "$werk/superpowers"
git clone --depth 1 --quiet https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git "$werk/uiux"
git clone --depth 1 --quiet https://github.com/remotion-dev/claude-code-plugin.git "$werk/remotion"
git clone --depth 1 --quiet https://github.com/JuliusBrussee/caveman.git "$werk/caveman"

sp_sha="$(git -C "$werk/superpowers" rev-parse --short HEAD)"
uiux_sha="$(git -C "$werk/uiux" rev-parse --short HEAD)"
rem_sha="$(git -C "$werk/remotion" rev-parse --short HEAD)"
cave_sha="$(git -C "$werk/caveman" rev-parse --short HEAD)"

echo "Oude kopie weghalen..."
if [ -d "$doel" ]; then
  for map in "$doel"/*/; do
    naam="$(basename "$map")"
    behouden=false
    # De +-vorm houdt een lege lijst stil; zonder dat valt set -u erover.
    for e in ${eigen[@]+"${eigen[@]}"}; do [ "$naam" = "$e" ] && behouden=true; done
    $behouden || rm -rf "$map"
  done
fi
mkdir -p "$doel"

echo "Neerzetten..."
cp -R "$werk/superpowers/skills/." "$doel/"
cp -R "$werk/uiux/.claude/skills/." "$doel/"
cp -R "$werk/remotion/skills/." "$doel/"
# Alleen de caveman-skill zelf, niet de rest van dat project (proxyserver,
# Go-binaries, browserextensie -- zie HERKOMST.md).
mkdir -p "$doel/caveman"
cp -R "$werk/caveman/skills/caveman/." "$doel/caveman/"

# ui-ux-pro-max levert een skill die simpelweg `design` heet. Claude heeft zelf
# ook een `design`-skill (het ontwerpcanvas), en twee skills met dezelfde naam
# betekent dat er eentje verliest. Deze krijgt daarom een eigen naam.
if [ -d "$doel/design" ]; then
  mv "$doel/design" "$doel/ui-ux-design"
  grep -rl 'skills/design/' "$doel/ui-ux-design" | while read -r f; do
    sed -i 's|skills/design/|skills/ui-ux-design/|g' "$f"
  done
  sed -i '0,/^name: design$/s||name: ui-ux-design|' "$doel/ui-ux-design/SKILL.md"
fi

# De ui-ux-skills verwijzen naar ~/.claude/skills/... omdat ze normaal per
# gebruiker geinstalleerd staan. Hier staan ze in de repo, dus het pad klopt niet.
grep -rl '~/\.claude/skills/' "$doel" 2>/dev/null | while read -r f; do
  sed -i 's|~/\.claude/skills/|.claude/skills/|g' "$f"
done

cat > "$doel/HERKOMST.md" <<HERKOMST
# Waar deze skills vandaan komen

Niet met de hand bijgehouden. Dit is een kopie, neergezet door
\`scripts/skills-bijwerken.sh\`. Bijwerken doe je door dat script te draaien,
niet door hier te typen. Zie [docs/claude-skills.md](../../docs/claude-skills.md)
voor waarom ze in de repo staan en niet in een marketplace.

Alles in deze map is geleend. Krijgt nativecontour een eigen skill, zet zijn
mapnaam dan in \`eigen=()\` bovenin het script, anders veegt de volgende
bijwerkronde hem weg.

| Map | Herkomst | Licentie | Commit |
|---|---|---|---|
| superpowers (14 skills) | [obra/superpowers](https://github.com/obra/superpowers) | MIT | \`$sp_sha\` |
| ui-ux-pro-max (7 skills) | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | \`$uiux_sha\` |
| remotion (12 skills) | [remotion-dev/claude-code-plugin](https://github.com/remotion-dev/claude-code-plugin) | MIT | \`$rem_sha\` |
| caveman (1 skill) | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | MIT | \`$cave_sha\` |

Bijgewerkt op $(date +%Y-%m-%d).

\`caveman\` is de uitzondering: alleen de map \`skills/caveman/\` uit dat project is
overgenomen, niet de rest. De bovenstroomse repo is verder een heel
software-project (proxyserver, Go-binaries, browserextensie, telemetrie) om die
ene modus te leveren als plugin met hooks; hier is het gewoon een SKILL.md, net
als de andere drie.

Twee dingen die het script aanpast aan de originelen, en waarom:

- \`design/\` heet hier \`ui-ux-design/\`. Claude heeft zelf al een skill die
  \`design\` heet (het ontwerpcanvas) en gelijke namen botsen.
- Paden die met \`~/.claude/skills/\` beginnen zijn \`.claude/skills/\` geworden.
  De originelen gaan ervan uit dat ze per gebruiker geinstalleerd staan; hier
  staan ze in de repo.
HERKOMST

echo
echo "Klaar: $(find "$doel" -name SKILL.md | wc -l) skills in .claude/skills/"
echo "  superpowers  $sp_sha"
echo "  ui-ux-pro-max $uiux_sha"
echo "  remotion     $rem_sha"
echo "  caveman      $cave_sha"
