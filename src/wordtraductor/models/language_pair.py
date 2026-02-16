from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguagePair:
    source_code: str
    target_code: str
    is_supported: bool
    confidence_score: float
    notes: str


SUPPORTED_LANGUAGES = {
    "en", "fr", "es", "de", "it", "pt", "ru", "ja", "zh", "ko",
    "ar", "hi", "nl", "pl", "tr", "vi", "th", "id", "fi", "sv",
    "no", "da", "cs", "sk", "hu", "ro", "el", "bg", "hr", "sr",
    "uk", "he", "fa", "ur", "bn", "ta", "te", "ml", "kn", "mr",
    "gu", "pa", "af", "am", "hy", "az", "eu", "ka", "gl", "eo",
    "et", "lt", "lv", "sl", "ms", "sw", "zu", "xh",
}
