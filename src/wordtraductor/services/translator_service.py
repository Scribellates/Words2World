from __future__ import annotations

from typing import Iterable

from google.cloud import translate_v2


class TranslatorService:
    def __init__(self, credentials) -> None:
        self._client = translate_v2.Client(credentials=credentials)

    def batch_texts(self, texts: Iterable[str], max_words: int) -> list[list[str]]:
        batches: list[list[str]] = []
        current: list[str] = []
        current_words = 0

        for text in texts:
            word_count = len(text.split())
            if current and current_words + word_count > max_words:
                batches.append(current)
                current = []
                current_words = 0
            current.append(text)
            current_words += word_count

        if current:
            batches.append(current)

        return batches

    def translate_batches(
        self,
        batches: list[list[str]],
        source_lang: str,
        target_lang: str,
    ) -> list[str]:
        translated: list[str] = []
        for batch in batches:
            result = self._client.translate(
                batch,
                source_language=source_lang,
                target_language=target_lang,
            )
            translated.extend([item["translatedText"] for item in result])
        return translated
