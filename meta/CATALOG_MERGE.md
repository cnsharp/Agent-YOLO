# Catalog merge algorithm (canonical reference)

This is the **single canonical description** of how each client (IntelliJ / VS / VS Code)
merges the remote catalog with its bundled catalog at startup. The three ports MUST
produce identical results. Keep this file in sync with `agents.schema.json` (`status`).

## Inputs

- `builtin` — the catalog bundled in the plugin (`agents.json` parsed at build time, legacy v1 shape).
  Built-in entries have no `status`; treat them as `"active"`.
- `remote` — the catalog fetched from the official URL at startup (v2 envelope `{schemaVersion, updatedAt, agents}`).
  Already unwrapped to the `agents` array and validated before this step.
- `installed` — set of `command` strings detected on the local PATH (from each end's install cache).
- `userAdded` — set of `id`s the user has explicitly added/configured in settings; these are never dropped (their field overrides live in each end's settings layer and are applied after the merge).

## Rules (in priority order)

1. **Seed with built-in.** `result` starts as a map of every `builtin` entry keyed by `id`
   (a remote omission never deletes a built-in agent — remote is an incremental overlay).
2. **Overlay each remote entry by `id`:**
   - If `id ∈ userAdded` → `result[id] = entry` — add/overlay it but do NOT apply the
     outdated filter (the user's own field overrides are applied later by each end's
     settings layer; the entry must still be present in the merged registry).
   - Else if `isOutdatedAndUninstalled(entry)` → **remove `id` from `result` entirely**
     (also drop the built-in copy of the same id) and skip this remote entry.
   - Else → `result[id] = entry` (override built-in, or add new).
3. **`isOutdatedAndUninstalled(entry)`** = BOTH conditions hold:
   - `entry.command ∉ installed` (not found on local PATH), AND
   - `status ∈ {"stale", "maintaining", "closed"}`.
   An installed outdated agent is kept so the user can still see/manage/uninstall it.
4. **User-added exemption** overrides rule 3's filter for any `id ∈ userAdded` (the entry is still added/overlaid by rule 2 — it is never silently skipped).

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
function mergeCatalogs(builtin, remote, installed, userAdded):
    result = { id -> entry } from builtin          # rule 1
    for entry in remote:                            # rule 2
        id = entry.id
        if id in userAdded:                         # rule 4
            result[id] = entry                      # keep it, but skip the outdated filter
            continue
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
