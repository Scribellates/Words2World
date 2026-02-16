from __future__ import annotations

import re

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024
FILE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{10,}$")
OUTPUT_NAME_PATTERN = re.compile(r"[^A-Za-z0-9 _()\-]")


def validate_file_id(file_id: str) -> None:
    if not file_id or not FILE_ID_PATTERN.fullmatch(file_id):
        raise ValueError("Invalid Google Drive file ID")


def validate_file_size(file_size_bytes: int) -> None:
    if file_size_bytes <= 0:
        raise ValueError("File size must be positive")
    if file_size_bytes > MAX_FILE_SIZE_BYTES:
        raise ValueError("File exceeds 25MB limit")


def validate_language_pair(
    source_lang: str,
    target_lang: str,
    supported_languages: set[str],
) -> None:
    if source_lang not in supported_languages or target_lang not in supported_languages:
        raise ValueError("Unsupported language code")
    if source_lang == target_lang:
        raise ValueError("Source and target languages must differ")


def validate_format(format_value, supported_formats) -> None:
    if format_value not in supported_formats:
        raise ValueError("Unsupported file format")


def sanitize_output_name(name: str) -> str:
    cleaned = OUTPUT_NAME_PATTERN.sub("_", name.strip())
    if not cleaned:
        raise ValueError("Output name cannot be empty")
    return cleaned
