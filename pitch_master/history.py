"""Pitch Master — Pitch History.

Save, load, and manage past pitches and audits.
"""

from __future__ import annotations

import json
import os
import datetime
from typing import Optional

from pitch_master.config import OUTPUT_DIR

HISTORY_DIR = os.path.join(OUTPUT_DIR, "history")
os.makedirs(HISTORY_DIR, exist_ok=True)


def _timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _now_iso() -> str:
    return datetime.datetime.now().isoformat()


def save_pitch(
    company_name: str,
    mode: str,
    content: str,
    pef_score: Optional[float] = None,
    pef_data: Optional[dict] = None,
    lang: str = "EN",
    metadata: Optional[dict] = None,
) -> str:
    """Save a pitch/audit to history. Returns the entry ID."""
    entry_id = f"{_timestamp()}_{company_name.replace(' ', '_')}"
    entry = {
        "id": entry_id,
        "company_name": company_name,
        "mode": mode,
        "content": content,
        "pef_score": pef_score,
        "pef_data": pef_data,
        "lang": lang,
        "metadata": metadata or {},
        "created_at": _now_iso(),
    }
    filepath = os.path.join(HISTORY_DIR, f"{entry_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    return entry_id


def load_pitch(entry_id: str) -> Optional[dict]:
    """Load a pitch by ID."""
    filepath = os.path.join(HISTORY_DIR, f"{entry_id}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_pitches(mode: Optional[str] = None) -> list[dict]:
    """List all saved pitches, newest first. Optionally filter by mode."""
    entries = []
    for filename in os.listdir(HISTORY_DIR):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(HISTORY_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            entry = json.load(f)
        if mode and entry.get("mode") != mode:
            continue
        entries.append(entry)
    entries.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return entries


def delete_pitch(entry_id: str) -> bool:
    """Delete a pitch by ID. Returns True if deleted."""
    filepath = os.path.join(HISTORY_DIR, f"{entry_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False


def get_stats() -> dict:
    """Get summary statistics of all saved pitches."""
    entries = list_pitches()
    if not entries:
        return {"total": 0, "build": 0, "audit": 0, "avg_pef": 0}

    build_count = sum(1 for e in entries if e.get("mode") == "build")
    audit_count = sum(1 for e in entries if e.get("mode") == "audit")
    pef_scores = [e["pef_score"] for e in entries if e.get("pef_score") is not None]
    avg_pef = sum(pef_scores) / len(pef_scores) if pef_scores else 0

    return {
        "total": len(entries),
        "build": build_count,
        "audit": audit_count,
        "avg_pef": round(avg_pef, 1),
        "pef_scores": pef_scores,
    }
