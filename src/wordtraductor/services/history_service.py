from __future__ import annotations

import json
from datetime import datetime

from wordtraductor.models.config import Config
from wordtraductor.models.translation_history import TranslationHistoryEntry


class HistoryService:
    def __init__(self, config: Config) -> None:
        self._path = config.history_path

    def load_entries(self) -> list[TranslationHistoryEntry]:
        if not self._path.exists():
            return []
        data = json.loads(self._path.read_text(encoding="utf-8"))
        entries = data.get("entries", [])
        return [TranslationHistoryEntry.from_dict(item) for item in entries]

    def save_entries(self, entries: list[TranslationHistoryEntry]) -> None:
        payload = {"entries": [entry.to_dict() for entry in entries]}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add_entry(self, entry: TranslationHistoryEntry) -> None:
        entries = self.load_entries()
        entries.insert(0, entry)
        self.save_entries(entries[:500])

    def list_recent(self, limit: int) -> list[TranslationHistoryEntry]:
        return self.load_entries()[:limit]

    def get_by_index(self, index: int) -> TranslationHistoryEntry:
        entries = self.load_entries()
        if index < 1 or index > len(entries):
            raise ValueError("History index out of range")
        return entries[index - 1]

    @staticmethod
    def create_entry(
        file_id: str,
        source_name: str,
        target_name: str,
        source_lang: str,
        target_lang: str,
        result_file_id: str | None,
        status: str,
    ) -> TranslationHistoryEntry:
        now = datetime.utcnow()
        return TranslationHistoryEntry(
            entry_id=now.strftime("history-%Y%m%d%H%M%S"),
            file_id=file_id,
            source_name=source_name,
            target_name=target_name,
            source_lang=source_lang,
            target_lang=target_lang,
            created_at=now,
            completed_at=now,
            result_file_id=result_file_id,
            status=status,
        )
