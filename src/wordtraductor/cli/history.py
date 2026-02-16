from __future__ import annotations

import click

from wordtraductor.services.history_service import HistoryService
from wordtraductor.utils.ads import render_ad
from wordtraductor.utils.config_loader import load_config


@click.command("history")
@click.option("--limit", default=10, show_default=True, help="Number of entries to show")
def history_command(limit: int) -> None:
    config = load_config()
    service = HistoryService(config)
    entries = service.list_recent(limit)

    if not entries:
        click.echo("No translation history found.")
        return

    click.echo("Recent Translations:")
    for idx, entry in enumerate(entries, start=1):
        click.echo(
            f"{idx}. {entry.source_name} ({entry.source_lang} -> {entry.target_lang}) "
            f"-> {entry.target_name}"
        )

    click.echo(render_ad())
