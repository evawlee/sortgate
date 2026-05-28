from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class BuilderSettings:
    quote_char: str = '"'
    max_field_length: int = 64
    default_direction: str = "asc"


def load_settings() -> BuilderSettings:
    s = BuilderSettings()
    qc = os.environ.get("SORTGATE_QUOTE_CHAR")
    if qc:
        s = BuilderSettings(
            quote_char=qc,
            max_field_length=s.max_field_length,
            default_direction=s.default_direction,
        )
    return s


SETTINGS = load_settings()
