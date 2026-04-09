from __future__ import annotations

import click

from wordtraductor.services.google_auth_service import GoogleAuthService
from wordtraductor.services.google_drive_service import GoogleDriveService
from wordtraductor.services.format_converter import FormatConverter
from wordtraductor.models.document_format import SUPPORTED_FORMATS
from wordtraductor.services.history_service import HistoryService
from wordtraductor.services.translation_workflow import TranslationWorkflow
from wordtraductor.services.translator_service import TranslatorService
from wordtraductor.services.word_parser import WordParser
from wordtraductor.utils.ads import render_ad
from wordtraductor.utils.config_loader import load_config
from wordtraductor.utils.formatters import progress_step
from wordtraductor.utils.logging import setup_logging

DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"


@click.command("translate")
@click.option("--source-doc", required=True, help="Google Drive file ID")
@click.option("--source-lang", required=True, help="Source language (ISO 639-1)")
@click.option("--target-lang", required=True, help="Target language (ISO 639-1)")
@click.option("--output-name", required=False, help="Custom output name (no .docx needed)")
@click.option("--overwrite", is_flag=True, default=False, help="Overwrite original document")
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logging")
def translate_command(
    source_doc: str,
    source_lang: str,
    target_lang: str,
    output_name: str | None,
    overwrite: bool,
    verbose: bool,
) -> None:
    config = load_config()
    logger = setup_logging(verbose or config.verbose)

    try:
        click.echo(progress_step(1, 5, "Authenticating with Google Drive"))
        creds = GoogleAuthService(config).get_credentials([DRIVE_SCOPE])

        drive_service = GoogleDriveService(creds)
        translator_service = TranslatorService()
        parser = WordParser()
        converter = FormatConverter()
        history = HistoryService(config)
        workflow = TranslationWorkflow(
            config, drive_service, translator_service, parser, converter, logger, history
        )

        click.echo(progress_step(2, 5, "Translating document"))
        result = workflow.translate_file(
            file_id=source_doc,
            source_lang=source_lang,
            target_lang=target_lang,
            output_name=output_name,
            overwrite=overwrite,
        )

        click.echo(progress_step(3, 5, "Upload complete"))
        click.echo(
            f"Translation complete. Output: {result['output_name']} (ID: {result['output_file_id']})"
        )
        click.echo(render_ad())
    except Exception as exc:  # noqa: BLE001
        logger.error("Translation failed: %s", exc)
        message = str(exc)
        if "format" in message.lower():
            supported = ", ".join(sorted(fmt.value for fmt in SUPPORTED_FORMATS))
            message = f"Unsupported file format. Supported: {supported}"
        click.echo(f"Error: {message}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    translate_command()
