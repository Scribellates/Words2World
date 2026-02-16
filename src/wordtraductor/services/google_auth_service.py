from __future__ import annotations

from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from wordtraductor.models.config import Config


class GoogleAuthService:
    def __init__(self, config: Config) -> None:
        self._config = config

    def get_credentials(self, scopes: Iterable[str]) -> Credentials:
        token_path = self._config.token_path
        creds = None

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), scopes=list(scopes))

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        if not creds or not creds.valid:
            client_secrets = self._require_client_secrets()
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), scopes=list(scopes))
            creds = flow.run_local_server(port=0)
            token_path.write_text(creds.to_json(), encoding="utf-8")

        return creds

    def _require_client_secrets(self) -> Path:
        if not self._config.client_secrets_path:
            raise ValueError(
                "Missing client secrets. Set WORDTRADUCTOR_CLIENT_SECRETS to the JSON path."
            )
        return self._config.client_secrets_path
