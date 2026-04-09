from __future__ import annotations

from enum import Enum


class DocumentFormat(Enum):
    DOCX = "docx"
    DOC = "doc"
    DOCM = "docm"
    GOOGLE_DOCS = "google-doc"


MIME_TO_FORMAT = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocumentFormat.DOCX,
    "application/msword": DocumentFormat.DOC,
    "application/vnd.ms-word.document.macroEnabled.12": DocumentFormat.DOCM,
    "application/vnd.google-apps.document": DocumentFormat.GOOGLE_DOCS,
}

SUPPORTED_FORMATS = {DocumentFormat.DOCX, DocumentFormat.DOC, DocumentFormat.DOCM, DocumentFormat.GOOGLE_DOCS}


def detect_format(filename: str, mime_type: str) -> DocumentFormat:
    if mime_type in MIME_TO_FORMAT:
        return MIME_TO_FORMAT[mime_type]

    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    for fmt in SUPPORTED_FORMATS:
        if fmt.value == ext:
            return fmt

    raise ValueError("Unsupported file format")
