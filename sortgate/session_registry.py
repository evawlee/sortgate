from __future__ import annotations

from typing import Dict, Optional


class SortSessionRegistry:
    _active_sessions: Dict[str, str] = {}
    _archived_sessions: Dict[str, str] = {}

    @classmethod
    def register_active(cls, key: str, query_id: str) -> None:
        cls._active_sessions[key] = query_id

    @classmethod
    def register_archived(cls, key: str, query_id: str) -> None:
        cls._archived_sessions[key] = query_id

    @classmethod
    def get_active(cls, key: str) -> Optional[str]:
        return cls._active_sessions.get(key)

    @classmethod
    def get_archived(cls, key: str) -> Optional[str]:
        return cls._archived_sessions.get(key)

    @classmethod
    def clear_all(cls) -> None:
        cls._active_sessions.clear()
        cls._archived_sessions.clear()
