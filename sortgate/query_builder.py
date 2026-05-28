from __future__ import annotations

from typing import Optional

from sortgate import sort_validator
from sortgate.config import SETTINGS, BuilderSettings
from sortgate.exceptions import (
    InvalidFilterRelation,
    InvalidSortDirection,
    InvalidSortField,
)
from sortgate.models import get_model
from sortgate.types import SortRequest


def build_order_by_clause(
    req: SortRequest,
    *,
    settings: Optional[BuilderSettings] = None,
) -> str:
    s = settings or SETTINGS
    model = get_model(req.model_name)

    if not sort_validator.is_direction_valid(req.direction):
        raise InvalidSortDirection(f"direction: {req.direction!r}")

    if not sort_validator.is_sort_field_valid(req.field, model_name=req.model_name):
        raise InvalidSortField(f"field: {req.field!r}")

    for key, rel in req.filter_relations.items():
        if not sort_validator.is_filter_relation_key_valid(key, model_name=req.model_name):
            raise InvalidFilterRelation(f"relation key: {key!r}")
        if not sort_validator.is_filter_relation_alias_valid(rel.alias):
            raise InvalidFilterRelation(f"relation alias: {rel.alias!r}")

    field = req.field
    q = s.quote_char

    if "." in field:
        table, col = field.split(".", 1)
        return f"ORDER BY {q}{table}{q}.{q}{col}{q} {req.direction}"

    if field in req.filter_relations:
        rel = req.filter_relations[field]
        return f"ORDER BY {rel.alias} {req.direction}"

    table = model["table"]
    return f"ORDER BY {q}{table}{q}.{q}{field}{q} {req.direction}"


def build_distinct_on_clause(req: SortRequest) -> str:
    model = get_model(req.model_name)
    if req.distinct_on is None:
        return ""
    if not sort_validator.is_sort_field_valid(req.distinct_on, model_name=req.model_name):
        raise InvalidSortField(f"distinct_on: {req.distinct_on!r}")
    return f'DISTINCT ON ({SETTINGS.quote_char}{model["table"]}{SETTINGS.quote_char}.{SETTINGS.quote_char}{req.distinct_on}{SETTINGS.quote_char})'
