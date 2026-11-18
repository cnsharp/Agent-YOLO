# Catalog merge algorithm (canonical reference)

This is the **single canonical description** of how each client (IntelliJ / VS / VS Code)
merges the remote catalog with its bundled catalog at startup. The three ports MUST
produce identical results. Keep this file in sync with `agents.schema.json` (`status`).

**Scope — this is stage A only.** The merge operates purely on the two *official*
catalogs (bundled + remote). User-added / user-configured agents live **only in local
settings** and never appear in the remote catalog; each end's existing settings layer
builds the final list as `registry agents + local overrides/additions` in stage B, so
a local agent can never be touched by the remote "outdated" filter. The merge therefore
takes no notion of "user added".

## Inputs

- `builtin` — the catalog bundled in the plugin (`agents.json`, now v2 with a `status` on every entry).
  Parsers must still accept legacy v1 arrays (entries there have no `status`; treat them as `"active"`) —
  v1 is read-only legacy input, never authored anew.
- `remote` — the catalog fetched from the official URL at startup (v2 envelope `{schemaVersion, updatedAt, agents}`).
  Already unwrapped to the `agents` array and validated before this step.
- `installed` — set of `command` strings detected on the local PATH (from each end's install cache).

## Rules (in priority order)

1. **Seed with built-in.** `result` starts as a map of every `builtin` entry keyed by `id`
   (a remote omission never deletes a built-in agent — remote is an incremental overlay).
2. **Overlay each remote entry by `id`:**
   - If `isOutdatedAndUninstalled(entry)` → **remove `id` from `result` entirely**
     (also drop the built-in copy of the same id) and skip this remote entry.
   - Else → `result[id] = entry` (override built-in, or add new).
3. **`isOutdatedAndUninstalled(entry)`** = BOTH conditions hold:
   - `entry.command ∉ installed` (not found on local PATH), AND
   - `status ∈ {"stale", "maintaining", "closed"}`.
   An installed outdated agent is kept so the user can still see/manage/uninstall it.

User-added / user-configured agents are **not an input here** — they are local-only and
are re-applied by each end's settings layer in stage B, after this merge.

## Guards

- `status` is whitelisted: any value outside `active|maintaining|stale|closed|unknown`
  is treated as `unknown` (never filtered).
- If `result` is empty after filtering → discard it and fall back to the full `builtin` list
  (never show an empty catalog).
- The merge depends on the async install scan. Run it only after the install set is ready;
  until then use the previously cached install set (otherwise an installed-but-not-yet-
  detected agent could be wrongly filtered).
- The merge is read-only over catalog fields and local install state — it never executes
  any remote content (install/update commands stay in the curated catalog and are trusted
  only because the URL is locked to the official source).

## Pseudocode

```
function mergeCatalogs(builtin, remote, installed):
    result = { id -> entry } from builtin          # rule 1
    for entry in remote:                            # rule 2
        id = entry.id
        if isOutdatedAndUninstalled(entry, installed):
            result.remove(id)                       # drop built-in copy too
            continue
        result[id] = entry                          # overlay / add
    if result is empty:                             # guard
        return builtin
    return values(result)

function isOutdatedAndUninstalled(entry, installed):
    OUTDATED = {"stale", "maintaining", "closed"}
    status = canonStatus(entry.status)              # unknown if not whitelisted
    return (entry.command not in installed) and (status in OUTDATED)

function canonStatus(s):
    return s if s in {"active","maintaining","stale","closed","unknown"} else "unknown"
```
