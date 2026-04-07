from __future__ import annotations

from typing import Iterable

import argostranslate.package
import argostranslate.translate


class TranslatorService:
    def __init__(self) -> None:
        self._installed: set[tuple[str, str]] = set()

    def _ensure_package(self, from_code: str, to_code: str) -> None:
        if (from_code, to_code) in self._installed:
            return

        installed_langs = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_langs if l.code == from_code), None)
        if from_lang:
            to_lang = next(
                (t for t in from_lang.translations_to if t.to_lang.code == to_code), None
            )
            if to_lang:
                self._installed.add((from_code, to_code))
                return

        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()
        pkg = next(
            (p for p in available if p.from_code == from_code and p.to_code == to_code),
            None,
        )
        if pkg is None:
            raise ValueError(
                f"No Argos Translate package available for {from_code} → {to_code}. "
                "Check supported pairs at https://www.argosopentech.com/argospm/index/"
            )
        argostranslate.package.install_from_path(pkg.download())
        self._installed.add((from_code, to_code))

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
        self._ensure_package(source_lang, target_lang)
        translated: list[str] = []
        for batch in batches:
            for text in batch:
                translated.append(
                    argostranslate.translate.translate(text, source_lang, target_lang)
                )
        return translated
