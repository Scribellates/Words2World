from __future__ import annotations

import io
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload


class GoogleDriveService:
    def __init__(self, credentials) -> None:
        self._service = build("drive", "v3", credentials=credentials)

    def get_metadata(self, file_id: str) -> dict[str, Any]:
        fields = "id,name,size,mimeType,createdTime,modifiedTime,parents"
        return (
            self._service.files()
            .get(fileId=file_id, fields=fields, supportsAllDrives=True)
            .execute()
        )

    def download_file(self, file_id: str) -> io.BytesIO:
        request = self._service.files().get_media(fileId=file_id, supportsAllDrives=True)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        buffer.seek(0)
        return buffer

    def upload_file(
        self,
        file_bytes: io.BytesIO,
        mime_type: str,
        name: str,
        folder_id: str | None = None,
        overwrite_file_id: str | None = None,
    ) -> dict[str, Any]:
        media = MediaIoBaseUpload(file_bytes, mimetype=mime_type, resumable=True)
        if overwrite_file_id:
            return (
                self._service.files()
                .update(
                    fileId=overwrite_file_id,
                    media_body=media,
                    supportsAllDrives=True,
                )
                .execute()
            )

        body = {"name": name}
        if folder_id:
            body["parents"] = [folder_id]

        return (
            self._service.files()
            .create(
                body=body,
                media_body=media,
                fields="id,name,parents",
                supportsAllDrives=True,
            )
            .execute()
        )
