from __future__ import annotations

import click

from wordtraductor.services.google_auth_service import GoogleAuthService
from wordtraductor.services.google_drive_service import GoogleDriveService
from wordtraductor.services.history_service import HistoryService
from wordtraductor.services.translation_workflow import TranslationWorkflow
from wordtraductor.services.translator_service import TranslatorService
from wordtraductor.services.word_parser import WordParser
from wordtraductor.services.format_converter import FormatConverter
from wordtraductor.utils.ads import render_ad
from wordtraductor.utils.config_loader import load_config
from wordtraductor.utils.logging import setup_logging

DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"


@click.command("reuse")
@click.argument("index", type=int)
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logging")
def reuse_command(index: int, verbose: bool) -> None:
    config = load_config()
    logger = setup_logging(verbose or config.verbose)
    history = HistoryService(config)

    entry = history.get_by_index(index)

    creds = GoogleAuthService(config).get_credentials([DRIVE_SCOPE])
    drive_service = GoogleDriveService(creds)
    translator_service = TranslatorService(creds)
    parser = WordParser()
    converter = FormatConverter()

    workflow = TranslationWorkflow(
        config, drive_service, translator_service, parser, converter, logger, history
    )

    workflow.translate_file(
        file_id=entry.file_id,
        source_lang=entry.source_lang,
        target_lang=entry.target_lang,
        output_name=None,
        overwrite=False,
    )

    click.echo("Translation triggered from history entry.")
    click.echo(render_ad())
