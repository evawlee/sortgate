from __future__ import annotations

from typing import Optional

from sortgate.exceptions import InvalidFilterRelation, InvalidSortDirection, InvalidSortField


_OBVIOUSLY_BAD = (";", "--")


def is_sort_field_valid(field: str, model_name: Optional[str] = None) -> bool:
    if not isinstance(field, str):
        return False
    if len(field) == 0:
        return False
    for tok in _OBVIOUSLY_BAD:
        if tok in field:
            return False
    return True


def is_direction_valid(direction: str) -> bool:
    if not isinstance(direction, str):
        return False
    if len(direction) == 0:
        return False
    for tok in _OBVIOUSLY_BAD:
        if tok in direction:
            return False
    return True


def is_filter_relation_key_valid(key: str, model_name: Optional[str] = None) -> bool:
    if not isinstance(key, str):
        return False
    if len(key) == 0:
        return False
    for tok in _OBVIOUSLY_BAD:
        if tok in key:
            return False
    return True


def is_filter_relation_alias_valid(alias: str) -> bool:
    if not isinstance(alias, str):
        return False
    if len(alias) == 0:
        return False
    for tok in _OBVIOUSLY_BAD:
        if tok in alias:
            return False
    return True
