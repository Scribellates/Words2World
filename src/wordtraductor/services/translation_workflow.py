from __future__ import annotations

import os
from datetime import datetime

from wordtraductor.models.config import Config
from wordtraductor.models.document import Document
from wordtraductor.models.document_format import SUPPORTED_FORMATS, DocumentFormat, detect_format
from wordtraductor.models.language_pair import SUPPORTED_LANGUAGES
from wordtraductor.models.translation_task import TranslationStatus, TranslationTask
from wordtraductor.services.format_converter import FormatConverter
from wordtraductor.services.google_drive_service import GoogleDriveService
from wordtraductor.services.history_service import HistoryService
from wordtraductor.services.translator_service import TranslatorService
from wordtraductor.services.word_parser import WordParser
from wordtraductor.utils.validators import (
    sanitize_output_name,
    validate_file_id,
    validate_file_size,
    validate_format,
    validate_language_pair,
)


class TranslationWorkflow:
    def __init__(
        self,
        config: Config,
        drive_service: GoogleDriveService,
        translator_service: TranslatorService,
        parser: WordParser,
        converter: FormatConverter,
        logger,
        history_service: HistoryService | None = None,
    ) -> None:
        self._config = config
        self._drive = drive_service
        self._translator = translator_service
        self._parser = parser
        self._converter = converter
        self._logger = logger
        self._history = history_service

    def translate_file(
        self,
        file_id: str,
        source_lang: str,
        target_lang: str,
        output_name: str | None,
        overwrite: bool,
    ) -> dict:
        validate_file_id(file_id)
        validate_language_pair(source_lang, target_lang, SUPPORTED_LANGUAGES)

        metadata = self._drive.get_metadata(file_id)
        file_size = int(metadata.get("size", 0))
        validate_file_size(file_size)

        document_format = detect_format(metadata.get("name", ""), metadata.get("mimeType", ""))
        validate_format(document_format, SUPPORTED_FORMATS)

        document = Document(
            file_id=file_id,
            file_name=metadata.get("name", "document.docx"),
            file_size_bytes=file_size,
            format=document_format,
            location_path=None,
            created_at=None,
            modified_at=None,
            mime_type=metadata.get("mimeType", ""),
        )

        task = TranslationTask(
            task_id="task-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            source_document=document,
            source_language=source_lang,
            target_language=target_lang,
            status=TranslationStatus.IN_PROGRESS,
            created_at=datetime.utcnow(),
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None,
            result_document_id=None,
            word_count=0,
            api_calls_made=0,
        )

        self._logger.info("Downloading document metadata and content")
        _DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        if document_format == DocumentFormat.GOOGLE_DOCS:
            file_bytes = self._drive.export_file(file_id)
            effective_format = DocumentFormat.DOCX.value
            effective_mime = _DOCX_MIME
        else:
            file_bytes = self._drive.download_file(file_id)
            effective_format = document.format.value
            effective_mime = document.mime_type
        docx = self._parser.load_with_conversion(
            file_bytes, effective_format, self._converter, self._config.tmp_dir
        )
        runs = self._parser.iter_runs(docx)
        texts = [run.text for run in runs]

        batches = self._translator.batch_texts(texts, self._config.max_batch_size)
        translations = self._translator.translate_batches(batches, source_lang, target_lang)

        self._parser.apply_translations(runs, translations)
        result_bytes = self._parser.to_bytes(docx)

        output_name_final = self._resolve_output_name(document.file_name, target_lang, output_name)

        upload_result = self._drive.upload_file(
            file_bytes=result_bytes,
            mime_type=effective_mime,
            name=output_name_final,
            folder_id=self._config.drive_folder_id,
            overwrite_file_id=file_id if (overwrite and document_format != DocumentFormat.GOOGLE_DOCS) else None,
        )

        task.completed_at = datetime.utcnow()
        task.status = TranslationStatus.COMPLETED
        task.result_document_id = upload_result.get("id")
        task.word_count = sum(len(text.split()) for text in texts)
        task.api_calls_made = len(batches)

        if self._history:
            entry = self._history.create_entry(
                file_id=file_id,
                source_name=document.file_name,
                target_name=output_name_final,
                source_lang=source_lang,
                target_lang=target_lang,
                result_file_id=task.result_document_id,
                status=task.status.value,
            )
            self._history.add_entry(entry)

        return {
            "task_id": task.task_id,
            "output_file_id": task.result_document_id,
            "output_name": output_name_final,
            "word_count": task.word_count,
            "api_calls": task.api_calls_made,
        }

    @staticmethod
    def _resolve_output_name(original_name: str, target_lang: str, output_name: str | None) -> str:
        if output_name:
            clean = sanitize_output_name(output_name)
            return clean if clean.lower().endswith(".docx") else f"{clean}.docx"

        base, _ = os.path.splitext(original_name)
        clean_base = sanitize_output_name(base or "translated")
        return f"{clean_base} - {target_lang}.docx"
