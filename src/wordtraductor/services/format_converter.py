from __future__ import annotations

import io
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


class FormatConverter:
    def convert_to_docx(self, file_bytes: io.BytesIO, extension: str, tmp_dir: Path) -> io.BytesIO:
        with TemporaryDirectory(dir=tmp_dir) as work_dir:
            input_path = Path(work_dir) / f"input.{extension}"
            output_path = Path(work_dir) / "input.docx"

            input_path.write_bytes(file_bytes.getvalue())

            subprocess.run(
                [
                    "libreoffice",
                    "--headless",
                    "--convert-to",
                    "docx",
                    str(input_path),
                    "--outdir",
                    str(Path(work_dir)),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if not output_path.exists():
                raise RuntimeError("LibreOffice conversion failed")

            return io.BytesIO(output_path.read_bytes())
