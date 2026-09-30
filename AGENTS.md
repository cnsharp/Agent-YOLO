# AGENTS.md — Agent YOLO Metadata Hub

## 1. Purpose

`Meta/` is the **single source of truth** for the Agent YOLO family's shared
metadata, configuration, and resource files. Agent YOLO ships on three IDE
platforms plus one upstream helper repo; instead of duplicating assets per
project, the shared ones live here and are ported outward.

## 2. Scope — the repositories

| Repo | Role |
| --- | --- |
| `YOLO-IntelliJ` | JetBrains / IntelliJ side. **Primary** reference platform. |
| `YOLO-VS` | Microsoft Visual Studio side. |
| `YOLO-VSC` | Visual Studio Code side. |
| `ai-agents-terminal-vsc` | Side project, **upstream of `YOLO-VSC`** (YOLO-VSC is a fork of it). No YOLO panel of its own. |

**Hard rule:** any agent or resource change for the **VS Code** side MUST be
made **first in `ai-agents-terminal-vsc`**, then ported to `YOLO-VSC`. Never edit the
VSC fork directly for shared assets.

## 3. Project paths — defaults, verify before use

The paths below are **relative to this `Meta/` directory** and assume the four
repos are **siblings of `Meta/`** (i.e. `Meta/` lives inside the shared
`Agent YOLO/` folder). **On other machines this layout may differ.**

- `YOLO-IntelliJ` → `../YOLO-IntelliJ`
- `YOLO-VS`       → `../YOLO-VS`
- `YOLO-VSC`      → `../YOLO-VSC`
- `ai-agents-terminal-vsc` → `../ai-agents-terminal-vsc`

### ⚠️ Mandatory path-handling rule
Before reading or writing any of the four sibling projects:
1. Check whether the default path **actually exists** on this machine
   (`test -d <path>` / `ls`).
2. **If it does NOT exist, STOP and ASK THE USER for the correct path.**
   - Do **not** guess or assume an alternative location.
   - Do **not** create the directory or `git init` a repo there.
   - Do **not** silently fall back to a different path.
3. Only proceed once you have a **confirmed, existing** path — either the
   default verified present, or a path supplied by the user.

## 4. What lives in `Meta/`

- `resources/agents.json` — the agent registry (id, displayName, command,
  baseArgs, skipFlag, resumeFlag, icon, url, install, skipEnv). Single source
  of truth for the agent list; **all three ends (IntelliJ, VS, VSC) now carry
  the same schema**. `icon` is a canonical path `/icons/agents/<id>.<ext>`;
  `baseArgs` is a shared launch default (each end may let the user override it);
  `install` is consumed only by the JVM ends.
- `resources/icons/agents/<id>.svg` | `.png` — bundled agent icons. SVG is the
  authored source; PNGs are also committed (see §6).
- `resources/icons/` (top level) — plugin icons (`pluginIcon*`) and the
  `resume*` / `skipY*` UI glyphs.
- `resources/messages/` — **i18n**, currently `YoloBundle.properties` +
  `YoloBundle_zh.properties`. **IntelliJ `.properties` is the i18n baseline.**
- `tools/link_patterns_source.py` — **canonical link RegExp source** (SINGLE
  SOURCE OF TRUTH). Holds every link-detecting pattern once, with a `<<EXT>>`
  placeholder for the programming-extension allowlist.
- `tools/gen_link_patterns.py` — generator. `python3 tools/gen_link_patterns.py
  --check` previews the blocks; `--write` injects them into the IntelliJ `.kt`
  and VS `.cs` targets, between the
  `// >>> YOLO_LINK_PATTERNS_START >>>` / `// <<< YOLO_LINK_PATTERNS_END <<<`
  markers. **Never hand-edit the marker regions** — they are regenerated.
- Generated per-end files (marker regions are machine-owned):
  `YOLO-IntelliJ/src/main/kotlin/com/cnsharp/yolo/panel/YoloLinkPatterns.kt`,
  `YOLO-VS/Links/YoloLinkPatterns.cs`.

## 5. Constraints (hard rules)

1. **Language / runtime** is decided by each sub-project; `Meta/` holds only
   shared assets, not build configuration.
2. **Keep icons and i18n text consistent across all platforms.**
   - **VSC ships only `.png` icons.** Its loader resolves the canonical `icon`
     path by basename and falls back to `<id>.png` when the referenced `.svg`
     is absent — so VSC consumes the same `agents.json` as the JVM ends without
     changing the `icon` field.
3. **i18n baseline = IntelliJ `.properties`.** Any change to IntelliJ's i18n
   resource files **MUST** be synced into `Meta/resources/messages/`.
4. **Link RegExp is generated from one Meta source.** Hand-editing the patterns
   in any end project is forbidden (it will be overwritten on regeneration).
   Workflow:
   - **IntelliJ is the regex source of truth.** If IntelliJ's
     `YoloLinkPatterns.kt` receives a fix, sync it **into
     `tools/link_patterns_source.py` first**, then regenerate — never the
     reverse.
   - Edit `tools/link_patterns_source.py` only (the `<<EXT>>` placeholder and
     the `PATTERNS` list). `EXT_VS_EXTRA` is the only legitimate per-platform
     delta (C#/VS-only extensions); everything else is shared.
   - Run `python3 tools/gen_link_patterns.py --write` to push the change to
     both `YOLO-IntelliJ` and `YOLO-VS`.
   - Confirm with `--check` that the generated blocks match both ends before
     committing. (Both ends are currently byte-for-byte in sync with Meta.)
5. **`agents.json` is the agent-registry source of truth — all three ends share
   one schema.** Edit `resources/agents.json` first, then **copy it verbatim** to
   all three ends:
   - `YOLO-IntelliJ/src/main/resources/agents.json`
   - `YOLO-VS/agents.json`
   - `ai-agents-terminal-vsc/agents.json` → then port to `YOLO-VSC/agents.json` (VS Code
     upstream-first, per §2).
   The `icon` field uses the canonical path `/icons/agents/<id>.<ext>` on every
   end. `YOLO-VS` maps it onto its embedded `Resources/icons/agents/` assets,
   and the VSC ends fall back to `<id>.png` under `media/agents/` (VSC ships
   PNGs only) — so **no per-end path editing is required**. Always include
   not-yet-enabled fields (e.g. `install`, `baseArgs`) — they are part of the
   registry. `baseArgs` is a shared launch default; VSC additionally lets the
   user override it per agent via settings.

## 6. Icon rules (summary)

Full detail: `.agents/skills/yolo-agent-icons/SKILL.md`. When adding /
replacing / removing an icon:

- **No hand-traced or hand-drawn SVGs** — use a genuine brand vector, or the
  real favicon (`.png`/`.ico`) when no clean SVG exists.
- **No text / wordmark** — symbol glyph only.
- **Keep original brand colors**; do not monochrome a colored mark.
- `<id>` must match `agents.json`; file at
  `resources/icons/agents/<id>.<svg|png>`.
- `_dark` variants only for monochrome/near-black bases (recolor to `#BDBDBD`);
  never for colored or two-tone marks, never for favicon PNGs.
- After changes: no dangling `icon` paths in `agents.json`; confirm the
  registry still compiles in the relevant platform project.

## 7. Common tasks (from the spec)

- **Add an agent:** entry in `agents.json` + icon in `resources/icons/agents/`;
  copy `agents.json` verbatim to the two JVM ends (§5.5); sync i18n if the UI
  exposes its name.
- **Remove an agent:** remove entry + icon; copy `agents.json`; clean any i18n
  references.
- **Update an icon:** follow §6; keep cross-platform consistency.
- **Fix a link RegExp:** per §5.4 — sync the fix into
  `tools/link_patterns_source.py`, then `python3 tools/gen_link_patterns.py
  --write`. IntelliJ is the source of truth.
- **Fix a common bug:** apply once in `Meta/` where shared, then port to each
  platform repo (VS Code side → `ai-agents-terminal-vsc` first).
