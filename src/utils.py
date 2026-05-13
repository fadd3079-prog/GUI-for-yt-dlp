from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any


DEFAULT_DOWNLOAD_DIR = Path(r"C:\Users\mlfad\downloads\ytdlp")
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def ensure_download_dir(path: Path = DEFAULT_DOWNLOAD_DIR) -> Path:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(f"Folder download tidak bisa dibuat: {path}. Detail: {exc}") from exc

    if not path.is_dir():
        raise RuntimeError(f"Path download bukan folder: {path}")

    return path


def command_to_display(command: list[str]) -> str:
    return subprocess.list2cmdline(command)


def check_tool(name: str, args: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [name, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            creationflags=CREATE_NO_WINDOW,
        )
    except FileNotFoundError:
        return {"name": name, "available": False, "error": f"{name} tidak ditemukan di PATH."}
    except subprocess.TimeoutExpired:
        return {"name": name, "available": False, "error": f"{name} tidak merespons."}

    output = (result.stdout or result.stderr or "").strip()
    first_line = output.splitlines()[0] if output else ""
    return {
        "name": name,
        "available": result.returncode == 0,
        "error": "" if result.returncode == 0 else (first_line or f"{name} gagal dijalankan."),
    }


def check_dependencies() -> dict[str, dict[str, Any]]:
    return {
        "yt-dlp": check_tool("yt-dlp", ["--version"]),
        "ffmpeg": check_tool("ffmpeg", ["-version"]),
        "ffprobe": check_tool("ffprobe", ["-version"]),
    }


def looks_like_url(value: str) -> bool:
    return bool(re.match(r"^https?://\S+$", value.strip(), flags=re.IGNORECASE))


def friendly_error_message(output: str) -> str:
    lower = output.lower()
    messages: list[str] = []

    if "http error 429" in lower or "too many requests" in lower:
        messages.append(
            "YouTube sedang membatasi request sementara. Coba lagi nanti, "
            "gunakan URL lain, atau kurangi percobaan berulang."
        )

    if "requested format is not available" in lower or "format is not available" in lower:
        messages.append("Format tidak tersedia. Coba pilih Best atau kualitas lain.")

    if not messages:
        return output

    return f"{output}\n\n" + "\n".join(messages)
