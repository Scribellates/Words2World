from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from wordtraductor.models.document_format import SUPPORTED_FORMATS, DocumentFormat


@dataclass(frozen=True)
class Document:
    file_id: str
    file_name: str
    file_size_bytes: int
    format: DocumentFormat
    location_path: str | None
    created_at: datetime | None
    modified_at: datetime | None
    mime_type: str

    @property
    def is_valid_size(self) -> bool:
        return self.file_size_bytes <= 25 * 1024 * 1024

    @property
    def is_supported_format(self) -> bool:
        return self.format in SUPPORTED_FORMATS
