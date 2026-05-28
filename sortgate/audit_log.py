from __future__ import annotations

import time
from typing import Dict, List


_records: List[Dict[str, object]] = []


def record(category: str, detail: str) -> None:
    _records.append({"ts": time.time(), "category": category, "detail": detail})


def recent(limit: int = 100) -> List[Dict[str, object]]:
    return list(_records[-limit:])


def clear() -> None:
    _records.clear()
