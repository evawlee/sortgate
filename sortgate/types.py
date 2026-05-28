from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class FilterRelation:
    alias: str
    base_field: str
    condition_payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SortRequest:
    model_name: str
    field: str
    direction: str = "asc"
    filter_relations: Dict[str, FilterRelation] = field(default_factory=dict)
    distinct_on: Optional[str] = None
