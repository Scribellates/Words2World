from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_BASE_DIR = Path.home() / ".wordtraductor"
DEFAULT_HISTORY_PATH = DEFAULT_BASE_DIR / "history.json"
DEFAULT_TOKEN_PATH = DEFAULT_BASE_DIR / ".google_credentials.json"
DEFAULT_MAX_BATCH_SIZE = 500

CLIENT_SECRETS_ENV = "WORDTRADUCTOR_CLIENT_SECRETS"
DRIVE_FOLDER_ENV = "WORDTRADUCTOR_DRIVE_FOLDER_ID"
VERBOSE_ENV = "WORDTRADUCTOR_VERBOSE"
MAX_BATCH_ENV = "WORDTRADUCTOR_MAX_BATCH_SIZE"
TMP_DIR_ENV = "WORDTRADUCTOR_TMP_DIR"


@dataclass(frozen=True)
class Config:
    drive_folder_id: str | None
    verbose: bool
    max_batch_size: int
    tmp_dir: Path
    base_dir: Path
    history_path: Path
    token_path: Path
    client_secrets_path: Path | None
