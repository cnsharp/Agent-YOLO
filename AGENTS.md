# AGENTS.md — Agent YOLO Metadata Hub

## 1. Purpose
`Meta/` is the **single source of truth** for the Agent YOLO family's shared metadata, config, and resources. Shared assets live here and are ported outward instead of being duplicated per project.

## 2. Repositories
| Repo | Role |
| --- | --- |
| `YOLO-IntelliJ` | IntelliJ side. **Primary** reference platform. |
| `YOLO-VS` | Visual Studio side. |
| `YOLO-VSC` | VS Code side. |
| `ai-agents-terminal-vsc` | Upstream of `YOLO-VSC` (YOLO-VSC is a fork). No YOLO panel of its own. |

**Hard rule:** any agent/resource change for the **VS Code** side MUST be made **first in `ai-agents-terminal-vsc`**, then ported to `YOLO-VSC`. Never edit the VSC fork directly for shared assets.

## 3. Paths — verify before use
Paths are relative to `Meta/` and assume the four repos are **siblings of `Meta/`** (inside the shared `Agent YOLO/` folder); **layout may differ on other machines**.
- `YOLO-IntelliJ` → `../YOLO-IntelliJ` · `YOLO-VS` → `../YOLO-VS` · `YOLO-VSC` → `../YOLO-VSC` · `ai-agents-terminal-vsc` → `../ai-agents-terminal-vsc`

**Mandatory path-handling rule:** before reading/writing any sibling, confirm the default path exists (`test -d`/`ls`). If it does **not**, **STOP and ASK THE USER** — do not guess, create the dir, `git init`, or silently fall back.

## 4. What lives in `Meta/`
Directory split: **`meta/` holds metadata** (the agent registry + its schema), **`resources/` holds bundled assets** (icons, i18n, plugin glyphs). Keep data and assets separate.
- `meta/agents.json` — agent registry, single source of truth for the agent list; **all three ends share one schema**. Top level is `{ "schemaVersion": 2, "updatedAt": "YYYY-MM-DD", "agents": [ … ] }`. Per-agent fields: `id`, `displayName`, `command`, `baseArgs`, `skipFlag`, `resumeFlag`, `icon`, `url`, `install`, `uninstall`, `skipEnv`, `status`, `latestVersion`, `platformSupport`. See `agents.schema.json` (JSON Schema 2020-12) and the schema-versioning rules below.
- `meta/agents.schema.json` — JSON Schema (draft 2020-12) for `agents.json`. Validates top-level shape, required fields, and enums (`status`, `platformSupport`, `install.type`, `uninstall` shape). Uses `additionalProperties: false`, so **any new field must be declared here too** or validation fails.
  - `icon` stores only the filename `<id>.<ext>`; each end prepends its own icon dir (`/icons/agents/` IntelliJ, `Resources/icons/agents/` VS, `media/agents/` VSC) — **no per-end path editing needed**. VSC ships PNGs only and falls back to `<id>.png` when the referenced `.svg` is absent.
  - `baseArgs` is a shared launch default (VSC also lets the user override it per agent); `install` is consumed only by the JVM ends.
  - `uninstall` — `{ cmd, cmdWin? }` shell command for removing the agent. **The uninstall channel must match the install channel**: `npm`/`pip`/`brew` installs use the matching `<mgr> uninstall`, while `shell` installs (`curl|bash` / `irm|iex`) delete the artifacts those scripts dropped (mac `rm`, Windows `Remove-Item`; `winget`/MSI/`uv tool`/WSL installs use their own inverse). `cmdWin` is omitted when `platformSupport.win32 = unsupported`, and when absent on a cross-platform package-manager install the `cmd` applies to both. No PATH/rc rollback and no `preserve` mechanism — "能卸载就行"; safety is in the command itself (delete exact artifacts, avoid whole config/history dirs like `~/.claude`, `~/.trae`, `~/.codex`).
  - `status` / `latestVersion` — vendor-lifecycle snapshot, collected from public release signals. `status` ∈ `active | maintaining | stale | unknown` (auto); company-level terminal states are deliberately **not** auto-assigned. `latestVersion` may be empty. Both decay over time — re-collect periodically.
  - `platformSupport` — `{ darwin, win32, linux }`, each `supported | unsupported | viaWsl`. Describes whether **this registry's install path** works on that OS, not the product's full platform reach; `viaWsl` = win32 runs through WSL, `unsupported` = no build for that OS.
  - ⚠️ **Schema-compat caveat:** the three ends still parse the old top-level **array** (= v1, no version field). Do **not** apply §5.4's verbatim copy until their parsers accept the v2 `{schemaVersion, updatedAt, agents}` object — copying the current shape would break all three. (Tracked as pending; three-end compatibility is deferred.)
  - **Schema versioning (L1)** — `schemaVersion` is the compatibility contract (integer), `updatedAt` is the data-snapshot date. They are deliberately separate:
    - **Breaking** — top-level shape change, delete/rename field, type change, tighten enum, make a field required → **bump `schemaVersion`**, update `agents.schema.json` (including its `$id` / `const`), and list every consumer's compatibility status. Consumers must reject unknown majors instead of failing deep inside a parser.
    - **Additive** — add an **optional** field, widen an enum → do **not** bump `schemaVersion`, but still declare the field in `agents.schema.json` (its `additionalProperties: false` will block it otherwise). Only `updatedAt` moves when `status`/`latestVersion` data is re-collected.
    - v1 = legacy bare array (three ends); v2 = current object. Validation (from repo root): `python3 -c "import json,jsonschema; jsonschema.Draft202012Validator(json.load(open('meta/agents.schema.json'))).validate(json.load(open('meta/agents.json')))"` (or any Draft 2020-12 validator).
- `resources/icons/agents/<id>.svg`|`.png` — bundled agent icons. SVG is the authored source; PNGs are also committed.
- `resources/icons/` (top level) — plugin icons (`pluginIcon*`) and `resume*`/`skipY*` UI glyphs.
- `resources/messages/` — i18n, currently `YoloBundle.properties` + `YoloBundle_zh.properties`. **IntelliJ `.properties` is the i18n baseline.**

## 5. Constraints (hard rules)
1. `Meta/` holds only shared assets, not build config (language/runtime is per sub-project).
2. **Link RegExp & gating logic are hand-maintained per edition — there is no Meta generator or shared source.** The patterns and gates (e.g. the ASCII / `looksLikeName` guards that stop TUI chrome like `● Bash` / `∴ Thought` from becoming links) live in each edition's own files; keep all three consistent by hand:
   - IntelliJ: `YOLO-IntelliJ/.../panel/YoloLinkPatterns.kt` + `FileLinkFilter`/`TypeLinkFilter` gates.
   - VS: `YOLO-VS/Links/YoloLinkPatterns.cs` + `Links/FileLinkFilter.cs`/`TypeLinkFilter.cs`.
   - VS Code: `YOLO-VSC/src/links/linkPatterns.ts` + `src/webview/panel.ts` gates. IntelliJ is the de-facto reference if they diverge.
3. **i18n baseline = IntelliJ `.properties`.** Any IntelliJ i18n change MUST be synced into `Meta/resources/messages/`.
4. **`agents.json` is the registry source of truth.** Edit it first, then **copy verbatim** to `YOLO-IntelliJ/src/main/resources/agents.json`, `YOLO-VS/agents.json`, and `ai-agents-terminal-vsc/agents.json` → port to `YOLO-VSC/agents.json` (upstream-first, §2). Always include not-yet-enabled fields (`install`, `baseArgs`).
5. Keep icons and i18n text consistent across all platforms.

## 6. Icon rules (summary)
Full detail: `.agents/skills/yolo-agent-icons/SKILL.md`. When adding/replacing/removing an icon:
- **No hand-traced or hand-drawn SVGs** — use a genuine brand vector, or the real favicon (`.png`/`.ico`) when no clean SVG exists.
- **No text / wordmark** — symbol glyph only.
- **Keep original brand colors**; do not monochrome a colored mark.
- `<id>` must match `agents.json`; file at `resources/icons/agents/<id>.<svg|png>`.
- `_dark` variants only for monochrome/near-black bases (recolor to `#BDBDBD`); never for colored/two-tone marks, never for favicon PNGs.
- After changes: no dangling `icon` paths in `agents.json`; confirm the registry still resolves on the relevant platform.

## 7. Common tasks
- **Add an agent:** entry in `agents.json` + icon in `resources/icons/agents/`; copy `agents.json` verbatim to the two JVM ends (§5.4); sync i18n if the UI exposes its name.
- **Remove an agent:** remove entry + icon; copy `agents.json`; clean any i18n references.
- **Update an icon:** follow §6; keep cross-platform consistency.
- **Fix a link RegExp / gate:** per §5.2 — edit the pattern/gate in **all three** editions by hand; keep them consistent.
- **Fix a common bug:** apply once in `Meta/` where shared, then port to each platform repo (VS Code side → `ai-agents-terminal-vsc` first).
