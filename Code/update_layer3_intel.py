from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "Data"
WATCHLIST_PATH = DATA_DIR / "layer3_watchlist.json"
INBOX_PATH = DATA_DIR / "layer3_source_inbox_2026.json"
CLAIMS_PATH = DATA_DIR / "layer3_extracted_claims_2026.json"
REGISTRY_PATH = DATA_DIR / "team_availability_2026.json"

DEFAULT_MODEL = os.environ.get("GROQ_MODEL") or "llama-3.3-70b-versatile"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

PRIORITY_SCORE = {
    "official": 5,
    "coach_quote": 4,
    "team_media": 4,
    "major_media": 3,
    "beat_report": 2,
    "speculative": 1,
    "manual": 3,
}

STATUS_VALUES = {
    "available",
    "doubtful",
    "ruled_out",
    "managed",
    "overseas_unavailable",
    "unknown",
}


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_html(raw: str) -> str:
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"\s+", " ", raw)
    return raw.strip()


def fetch_url(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "CreaseIQ-Layer3-Intel/1.0 (+https://creaseiq.onrender.com)",
            "Accept": "text/html,application/xml,application/rss+xml,application/atom+xml;q=0.9,*/*;q=0.8",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def looks_like_rss(text: str) -> bool:
    prefix = text.lstrip()[:200].lower()
    return prefix.startswith("<?xml") or "<rss" in prefix or "<feed" in prefix


def parse_rss_items(source: dict[str, Any], raw_text: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    root = ET.fromstring(raw_text)
    for item in root.findall(".//item")[:20]:
      title = (item.findtext("title") or "").strip()
      link = (item.findtext("link") or "").strip()
      description = (item.findtext("description") or "").strip()
      pub_date = (item.findtext("pubDate") or "").strip()
      if not title and not description:
          continue
      items.append(
          {
              "title": title or source["name"],
              "url": link or source["url"],
              "published_at": pub_date,
              "raw_text": strip_html(description),
          }
      )
    return items


def parse_web_item(source: dict[str, Any], raw_text: str) -> list[dict[str, Any]]:
    title_match = re.search(r"<title>(.*?)</title>", raw_text, flags=re.IGNORECASE | re.DOTALL)
    title = strip_html(title_match.group(1)) if title_match else source["name"]
    body = strip_html(raw_text)[:12000]
    return [
        {
            "title": title,
            "url": source["url"],
            "published_at": "",
            "raw_text": body,
        }
    ]


def source_item_id(source_id: str, url: str, title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", f"{source_id}_{title}_{urlparse(url).path}".lower()).strip("_")
    return slug[:120]


def team_scope_text(source: dict[str, Any]) -> list[str]:
    return [str(team).upper() for team in source.get("team_scope", [])]


def ingest_sources() -> list[dict[str, Any]]:
    watchlist = load_json(WATCHLIST_PATH, [])
    inbox = load_json(INBOX_PATH, [])
    existing_ids = {item["source_item_id"] for item in inbox}
    new_items: list[dict[str, Any]] = []

    for source in watchlist:
        if not source.get("enabled"):
            continue
        if source.get("source_type") == "manual":
            continue
        url = str(source.get("url") or "").strip()
        if not url:
            continue

        try:
            raw_text = fetch_url(url)
        except (HTTPError, URLError) as exc:
            print(f"[Layer3] fetch failed for {source['source_id']}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"[Layer3] unexpected fetch failure for {source['source_id']}: {exc}")
            continue

        parsed_items = parse_rss_items(source, raw_text) if looks_like_rss(raw_text) else parse_web_item(source, raw_text)
        for row in parsed_items:
            item_id = source_item_id(source["source_id"], row["url"], row["title"])
            if item_id in existing_ids:
                continue
            entry = {
                "source_item_id": item_id,
                "source_id": source["source_id"],
                "source_name": source["name"],
                "source_type": source["source_type"],
                "priority": source.get("priority", "major_media"),
                "team_scope": team_scope_text(source),
                "title": row["title"],
                "url": row["url"],
                "published_at": row["published_at"],
                "fetched_at": utc_now_iso(),
                "raw_text": row["raw_text"],
                "status": "unprocessed",
            }
            inbox.append(entry)
            new_items.append(entry)
            existing_ids.add(item_id)

    save_json(INBOX_PATH, inbox)
    return new_items


def build_extraction_prompt(source_item: dict[str, Any]) -> tuple[str, str]:
    system = (
        "You are extracting cricket player availability intelligence from a source item for an IPL analytics product. "
        "Return only JSON. Extract only explicit or strongly implied availability/selection information. "
        "Do not invent injuries or selection calls. Use these status values only: "
        "available, doubtful, ruled_out, managed, overseas_unavailable, unknown. "
        "Use these confidence values only: official, coach_quote, team_media, major_media, beat_report, speculative. "
        "Return a JSON array. Each row must contain: player, team, status, confidence, selection_probability, "
        "expected_absence_window, replacement_candidates, note."
    )
    user = json.dumps(
        {
            "source_name": source_item["source_name"],
            "priority": source_item["priority"],
            "team_scope": source_item["team_scope"],
            "title": source_item["title"],
            "published_at": source_item["published_at"],
            "url": source_item["url"],
            "raw_text": source_item["raw_text"][:9000],
        },
        ensure_ascii=False,
    )
    return system, user


def groq_extract_claims(source_item: dict[str, Any]) -> list[dict[str, Any]]:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured")

    system_prompt, user_content = build_extraction_prompt(source_item)
    body = {
        "model": DEFAULT_MODEL,
        "max_tokens": 1400,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }
    request = Request(
        GROQ_API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "User-Agent": "CreaseIQ-Layer3-Intel/1.0",
        },
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        payload_raw = json.loads(response.read().decode("utf-8"))
    content = payload_raw["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        content = content.rsplit("```", 1)[0].strip()
    rows = json.loads(content)
    if not isinstance(rows, list):
        raise ValueError("Groq extraction did not return a JSON array")
    return rows


def extract_claims(limit: int | None = None) -> list[dict[str, Any]]:
    inbox = load_json(INBOX_PATH, [])
    claims = load_json(CLAIMS_PATH, [])
    extracted: list[dict[str, Any]] = []

    pending = [item for item in inbox if item.get("status") != "processed"]
    if limit is not None:
        pending = pending[:limit]

    for item in pending:
        if not GROQ_API_KEY:
            item["status"] = "pending_groq"
            continue
        try:
            rows = groq_extract_claims(item)
        except Exception as exc:  # noqa: BLE001
            item["status"] = "extract_failed"
            item["extract_error"] = str(exc)
            continue

        for idx, row in enumerate(rows):
            claim = {
                "claim_id": f"{item['source_item_id']}_claim_{idx + 1}",
                "source_item_id": item["source_item_id"],
                "source_id": item["source_id"],
                "source_name": item["source_name"],
                "priority": item["priority"],
                "player": str(row.get("player") or "").strip(),
                "team": str(row.get("team") or "").strip().upper(),
                "status": str(row.get("status") or "unknown").strip(),
                "confidence": str(row.get("confidence") or item["priority"]).strip(),
                "selection_probability": float(row.get("selection_probability") or 0),
                "expected_absence_window": row.get("expected_absence_window"),
                "replacement_candidates": row.get("replacement_candidates") or [],
                "note": str(row.get("note") or "").strip(),
                "source_date": item.get("published_at") or item.get("fetched_at"),
                "extracted_at": utc_now_iso(),
            }
            if claim["player"]:
                claims.append(claim)
                extracted.append(claim)
        item["status"] = "processed"

    save_json(INBOX_PATH, inbox)
    save_json(CLAIMS_PATH, claims)
    return extracted


def resolve_registry() -> list[dict[str, Any]]:
    claims = load_json(CLAIMS_PATH, [])
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        player = str(claim.get("player") or "").strip()
        team = str(claim.get("team") or "").strip().upper()
        if not player or not team:
            continue
        grouped[(player, team)].append(claim)

    resolved: list[dict[str, Any]] = []
    for (player, team), rows in grouped.items():
        rows.sort(
            key=lambda row: (
                PRIORITY_SCORE.get(str(row.get("confidence") or row.get("priority")), 0),
                str(row.get("source_date") or ""),
            ),
            reverse=True,
        )
        best = rows[0]
        replacement_candidates: list[str] = []
        for row in rows:
            for candidate in row.get("replacement_candidates") or []:
                name = str(candidate).strip()
                if name and name not in replacement_candidates:
                    replacement_candidates.append(name)

        resolved.append(
            {
                "player": player,
                "team": team,
                "status": best["status"] if best["status"] in STATUS_VALUES else "unknown",
                "confidence": best.get("confidence") or best.get("priority") or "major_media",
                "selection_probability": float(best.get("selection_probability") or 0),
                "best_source": best.get("source_name", ""),
                "source_date": best.get("source_date", ""),
                "expected_absence_window": best.get("expected_absence_window"),
                "replacement_candidates": replacement_candidates,
                "note": best.get("note", ""),
            }
        )

    resolved.sort(key=lambda row: (row["team"], row["player"]))
    save_json(REGISTRY_PATH, resolved)
    return resolved


def print_summary(new_items: list[dict[str, Any]], extracted: list[dict[str, Any]], resolved: list[dict[str, Any]]) -> None:
    print(f"[Layer3] new source items: {len(new_items)}")
    print(f"[Layer3] extracted claims: {len(extracted)}")
    print(f"[Layer3] registry rows: {len(resolved)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Layer 3 availability intelligence for CreaseIQ.")
    parser.add_argument("--ingest-only", action="store_true", help="Fetch sources into inbox only.")
    parser.add_argument("--extract-only", action="store_true", help="Run Groq extraction on inbox only.")
    parser.add_argument("--resolve-only", action="store_true", help="Resolve claims into registry only.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of inbox items processed during extraction.")
    args = parser.parse_args()

    new_items: list[dict[str, Any]] = []
    extracted: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []

    if args.extract_only:
        extracted = extract_claims(limit=args.limit)
        print_summary(new_items, extracted, resolved)
        return
    if args.resolve_only:
        resolved = resolve_registry()
        print_summary(new_items, extracted, resolved)
        return

    if not args.extract_only and not args.resolve_only:
        new_items = ingest_sources()
        if args.ingest_only:
            print_summary(new_items, extracted, resolved)
            return
        extracted = extract_claims(limit=args.limit)
        resolved = resolve_registry()
        print_summary(new_items, extracted, resolved)


if __name__ == "__main__":
    main()
