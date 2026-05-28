from __future__ import annotations

from typing import Dict, FrozenSet, TypedDict


class ModelMeta(TypedDict):
    table: str
    sortable_fields: FrozenSet[str]
    all_columns: FrozenSet[str]


ARTICLE_MODEL: ModelMeta = {
    "table": "ordering_article",
    "sortable_fields": frozenset({"id", "headline", "pub_date", "author_id", "slug"}),
    "all_columns": frozenset({
        "id", "headline", "pub_date", "author_id", "slug",
        "draft_token", "internal_review_notes",
    }),
}

AUTHOR_MODEL: ModelMeta = {
    "table": "ordering_author",
    "sortable_fields": frozenset({"id", "name", "joined_at"}),
    "all_columns": frozenset({
        "id", "name", "joined_at", "internal_email", "phone",
    }),
}

COMMENT_MODEL: ModelMeta = {
    "table": "ordering_comment",
    "sortable_fields": frozenset({"id", "posted_at", "article_id"}),
    "all_columns": frozenset({
        "id", "posted_at", "article_id", "ip_address",
    }),
}

MODELS: Dict[str, ModelMeta] = {
    "Article": ARTICLE_MODEL,
    "Author": AUTHOR_MODEL,
    "Comment": COMMENT_MODEL,
}


def get_model(name: str) -> ModelMeta:
    from sortgate.exceptions import UnknownModel
    if name not in MODELS:
        raise UnknownModel(f"unknown model: {name!r}")
    return MODELS[name]
