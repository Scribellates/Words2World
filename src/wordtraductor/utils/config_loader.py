from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from wordtraductor.models.config import (
    CLIENT_SECRETS_ENV,
    DEFAULT_BASE_DIR,
    DEFAULT_HISTORY_PATH,
    DEFAULT_MAX_BATCH_SIZE,
    DEFAULT_TOKEN_PATH,
    DRIVE_FOLDER_ENV,
    MAX_BATCH_ENV,
    TMP_DIR_ENV,
    VERBOSE_ENV,
    Config,
)


def _parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def ensure_base_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_config() -> Config:
    load_dotenv()

    base_dir = DEFAULT_BASE_DIR
    ensure_base_dir(base_dir)

    drive_folder_id = os.getenv(DRIVE_FOLDER_ENV)
    verbose = _parse_bool(os.getenv(VERBOSE_ENV))

    max_batch_raw = os.getenv(MAX_BATCH_ENV)
    max_batch_size = DEFAULT_MAX_BATCH_SIZE
    if max_batch_raw:
        try:
            max_batch_size = int(max_batch_raw)
        except ValueError:
            max_batch_size = DEFAULT_MAX_BATCH_SIZE

    tmp_dir = Path(os.getenv(TMP_DIR_ENV, str(base_dir / "tmp")))
    tmp_dir.mkdir(parents=True, exist_ok=True)

    history_path = Path(str(DEFAULT_HISTORY_PATH))
    token_path = Path(str(DEFAULT_TOKEN_PATH))

    client_secrets_raw = os.getenv(CLIENT_SECRETS_ENV)
    client_secrets_path = Path(client_secrets_raw) if client_secrets_raw else None

    return Config(
        drive_folder_id=drive_folder_id,
        verbose=verbose,
        max_batch_size=max_batch_size,
        tmp_dir=tmp_dir,
        base_dir=base_dir,
        history_path=history_path,
        token_path=token_path,
        client_secrets_path=client_secrets_path,
    )
