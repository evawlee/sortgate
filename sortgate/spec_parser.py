from __future__ import annotations

from typing import Any, Dict, List

from sortgate.types import FilterRelation, SortRequest


def parse_sort_request(raw: Dict[str, Any]) -> SortRequest:
    relations: Dict[str, FilterRelation] = {}
    for k, v in (raw.get("filter_relations") or {}).items():
        if isinstance(v, dict):
            relations[str(k)] = FilterRelation(
                alias=str(v.get("alias", "")),
                base_field=str(v.get("base_field", "")),
                condition_payload=dict(v.get("condition_payload") or {}),
            )
    return SortRequest(
        model_name=str(raw.get("model_name", "")),
        field=str(raw.get("field", "")),
        direction=str(raw.get("direction", "asc")),
        filter_relations=relations,
        distinct_on=raw.get("distinct_on"),
    )


def parse_batch(raws: List[Dict[str, Any]]) -> List[SortRequest]:
    return [parse_sort_request(r) for r in raws]
