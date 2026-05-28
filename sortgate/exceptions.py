from __future__ import annotations


class SortgateError(Exception):
    pass


class InvalidSortField(SortgateError):
    pass


class InvalidSortDirection(SortgateError):
    pass


class InvalidFilterRelation(SortgateError):
    pass


class UnknownModel(SortgateError):
    pass
