from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TranslationHistoryEntry:
    entry_id: str
    file_id: str
    source_name: str
    target_name: str
    source_lang: str
    target_lang: str
    created_at: datetime
    completed_at: datetime | None
    result_file_id: str | None
    status: str

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "file_id": self.file_id,
            "source_name": self.source_name,
            "target_name": self.target_name,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result_file_id": self.result_file_id,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "TranslationHistoryEntry":
        return TranslationHistoryEntry(
            entry_id=data["entry_id"],
            file_id=data["file_id"],
            source_name=data["source_name"],
            target_name=data["target_name"],
            source_lang=data["source_lang"],
            target_lang=data["target_lang"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            result_file_id=data.get("result_file_id"),
            status=data["status"],
        )
