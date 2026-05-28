import pytest

from sortgate import audit_log, sort_validator
from sortgate.config import BuilderSettings
from sortgate.exceptions import (
    InvalidFilterRelation,
    InvalidSortDirection,
    InvalidSortField,
    UnknownModel,
)
from sortgate.query_builder import build_distinct_on_clause, build_order_by_clause
from sortgate.session_registry import SortSessionRegistry
from sortgate.spec_parser import parse_sort_request
from sortgate.types import FilterRelation, SortRequest


@pytest.fixture(autouse=True)
def reset_state():
    SortSessionRegistry.clear_all()
    audit_log.clear()
    yield
    SortSessionRegistry.clear_all()
    audit_log.clear()


@pytest.fixture
def settings():
    return BuilderSettings(quote_char='"', max_field_length=64, default_direction="asc")


@pytest.mark.parametrize("field", ["id", "headline", "pub_date", "author_id", "slug"])
def test_article_sortable_field_accepted(settings, field):
    req = SortRequest(model_name="Article", field=field, direction="asc")
    clause = build_order_by_clause(req, settings=settings)
    assert "ORDER BY" in clause
    assert field in clause


@pytest.mark.parametrize("direction", ["asc", "desc"])
def test_known_direction_accepted(settings, direction):
    req = SortRequest(model_name="Article", field="id", direction=direction)
    clause = build_order_by_clause(req, settings=settings)
    assert direction in clause


def test_unknown_model_rejected(settings):
    req = SortRequest(model_name="Ghost", field="id", direction="asc")
    with pytest.raises(UnknownModel):
        build_order_by_clause(req, settings=settings)


def test_obvious_semicolon_in_field_rejected(settings):
    req = SortRequest(model_name="Article", field="id; DROP TABLE ordering_article", direction="asc")
    with pytest.raises(InvalidSortField):
        build_order_by_clause(req, settings=settings)


def test_obvious_comment_token_in_direction_rejected(settings):
    req = SortRequest(model_name="Article", field="id", direction="asc--")
    with pytest.raises(InvalidSortDirection):
        build_order_by_clause(req, settings=settings)


def test_session_registry_two_store_independence():
    SortSessionRegistry.register_active("k1", "q-1")
    SortSessionRegistry.register_archived("k2", "q-2")
    assert SortSessionRegistry.get_active("k1") == "q-1"
    assert SortSessionRegistry.get_archived("k2") == "q-2"
    assert SortSessionRegistry.get_active("k2") is None
    assert SortSessionRegistry.get_archived("k1") is None


def test_spec_parser_round_trip():
    raw = {
        "model_name": "Article",
        "field": "pub_date",
        "direction": "desc",
        "filter_relations": {
            "author_rel": {
                "alias": "ord_a",
                "base_field": "author_id",
                "condition_payload": {"active": True},
            }
        },
        "distinct_on": "author_id",
    }
    req = parse_sort_request(raw)
    assert req.model_name == "Article"
    assert req.field == "pub_date"
    assert "author_rel" in req.filter_relations
    assert req.filter_relations["author_rel"].alias == "ord_a"


def test_distinct_on_accepts_sortable_field(settings):
    req = SortRequest(model_name="Article", field="id", direction="asc", distinct_on="author_id")
    clause = build_distinct_on_clause(req)
    assert "DISTINCT ON" in clause
    assert "author_id" in clause


def test_filter_relation_with_clean_key_and_alias(settings):
    fr = {"author_rel": FilterRelation(alias="ord_a", base_field="author_id")}
    req = SortRequest(model_name="Article", field="author_rel", direction="asc", filter_relations=fr)
    clause = build_order_by_clause(req, settings=settings)
    assert "ord_a" in clause
