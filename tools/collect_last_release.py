#!/usr/bin/env python3
"""Re-collect `lastReleaseAt` (UTC+0) for every agent in meta/agents.json.

`lastReleaseAt` is the timestamp of the agent's most recent UPSTREAM release,
probed from public release signals. It is a snapshot and decays over time — run
this periodically (AGENTS.md §4 "re-collect periodically"). An agent with no
queryable source keeps an empty string.

Signal priority, derived from the entry itself (no hand-maintained list):
  1. install.latest.npm            -> npm registry `time[latest]`
  2. install.latest.github         -> GitHub API `pushed_at`
  3. install.latest.pypi           -> PyPI `releases[*].upload_time_iso_8601`
  4. install.type == npm + pkg     -> npm registry
  5. install.type == pip  + pkg    -> PyPI
  6. otherwise                     -> empty (web-scraped / brew / unknown)

Only the standard library is used. Writes meta/agents.json back in its existing
2-space-indent format (json.dumps is byte-identical to the authored file) and
bumps top-level updatedAt to today (UTC date).

Usage:  python3 tools/collect_last_release.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "meta" / "agents.json"
TIMEOUT = 15
WORKERS = 6
UA = "agent-yolo-catalog-collector/1.0"


def get_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None


def to_utc_z(value: str | None) -> str:
    """Normalise an ISO-8601 timestamp to `YYYY-MM-DDTHH:mm:ssZ` (UTC+0)."""
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return ""


def npm_latest_time(pkg: str) -> str:
    quoted = urllib.parse.quote(pkg, safe="@")
    data = get_json(f"https://registry.npmjs.org/{quoted}")
    if not data:
        return ""
    times = data.get("time") or {}
    latest = (data.get("dist-tags") or {}).get("latest")
    if latest and latest in times:
        return to_utc_z(times[latest])
    # Fall back to the newest release timestamp (skip the metadata keys).
    candidates = [v for k, v in times.items() if k not in ("created", "modified")]
    return to_utc_z(max(candidates)) if candidates else ""


def github_pushed_at(repo: str) -> str:
    data = get_json(f"https://api.github.com/repos/{urllib.parse.quote(repo, safe='/')}")
    return to_utc_z((data or {}).get("pushed_at"))


def pypi_latest_time(pkg: str) -> str:
    data = get_json(f"https://pypi.org/pypi/{urllib.parse.quote(pkg, safe='')}/json")
    if not data:
        return ""
    stamps = []
    for files in (data.get("releases") or {}).values():
        for f in files or []:
            v = to_utc_z(f.get("upload_time_iso_8601"))
            if v:
                stamps.append(v)
    return max(stamps) if stamps else ""


def probe(agent: dict) -> tuple[str, str]:
    """Return (id, lastReleaseAt)."""
    aid = agent.get("id", "")
    install = agent.get("install") or {}
    latest = install.get("latest") or {}
    pkg = install.get("pkg") or ""
    itype = install.get("type") or ""

    try:
        if isinstance(latest.get("npm"), str) and latest["npm"]:
            return aid, npm_latest_time(latest["npm"])
        if isinstance(latest.get("github"), str) and latest["github"]:
            return aid, github_pushed_at(latest["github"])
        pypi = latest.get("pypi") if isinstance(latest.get("pypi"), str) else (pkg if itype == "pip" else "")
        if pypi:
            return aid, pypi_latest_time(pypi)
        if itype == "npm" and pkg:
            return aid, npm_latest_time(pkg)
    except Exception as exc:  # a single bad source must not abort the run
        print(f"  ! {aid}: {exc}", file=sys.stderr)
    return aid, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print results without writing the catalog")
    args = ap.parse_args()

    raw = CATALOG.read_text(encoding="utf-8")
    data = json.loads(raw)
    agents = data["agents"]

    results: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(probe, a): a.get("id", "") for a in agents}
        for fut in as_completed(futures):
            aid, value = fut.result()
            results[aid] = value

    filled = sum(1 for v in results.values() if v)
    print(f"probed {len(agents)} agents: {filled} with lastReleaseAt, {len(agents) - filled} empty")

    for a in agents:
        a["lastReleaseAt"] = results.get(a.get("id", ""), "")
    data["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if args.dry_run:
        for a in agents[:8]:
            print(f"  {a['id']:20s} {a['lastReleaseAt'] or '(empty)'}")
        return 0

    out = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    CATALOG.write_text(out, encoding="utf-8")
    print(f"wrote {CATALOG} (updatedAt={data['updatedAt']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
