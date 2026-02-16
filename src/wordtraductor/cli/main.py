from __future__ import annotations

import click

from wordtraductor.cli.history import history_command
from wordtraductor.cli.reuse import reuse_command
from wordtraductor.cli.translate import translate_command


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
def main() -> None:
    """WordTraductor command line interface."""


main.add_command(translate_command)
main.add_command(history_command)
main.add_command(reuse_command)


if __name__ == "__main__":
    main()
