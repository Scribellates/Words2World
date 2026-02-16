from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from wordtraductor.models.document import Document


class TranslationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TranslationTask:
    task_id: str
    source_document: Document
    source_language: str
    target_language: str
    status: TranslationStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    result_document_id: str | None
    word_count: int
    api_calls_made: int

    @property
    def duration_seconds(self) -> float | None:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
