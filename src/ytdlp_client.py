from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any, Callable


DEFAULT_DOWNLOAD_DIR = Path(r"C:\Users\mlfad\downloads\ytdlp")
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
LogCallback = Callable[[str], None]


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


def _path_from_line(line: str, output_dir: Path) -> Path | None:
    text = line.strip().strip('"')
    if not text:
        return None

    prefixes = [
        "[download] Destination:",
        "[Merger] Merging formats into",
        "[ExtractAudio] Destination:",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix) :].strip().strip('"')
            break
    else:
        already_downloaded = " has already been downloaded"
        if text.startswith("[download] ") and already_downloaded in text:
            text = text[len("[download] ") : text.index(already_downloaded)].strip().strip('"')

    try:
        candidate = Path(text)
    except OSError:
        return None

    if not candidate.is_absolute():
        return None

    try:
        candidate.resolve().relative_to(output_dir.resolve())
    except (OSError, ValueError):
        return None

    return candidate


def _find_newest_download(output_dir: Path, started_at: float) -> Path | None:
    ignored_suffixes = {".part", ".tmp", ".ytdl"}
    candidates: list[Path] = []
    for path in output_dir.glob("*"):
        if not path.is_file() or path.suffix.lower() in ignored_suffixes:
            continue
        try:
            if path.stat().st_mtime >= started_at - 2:
                candidates.append(path)
        except OSError:
            continue
    if not candidates:
        return None
    return max(candidates, key=lambda item: item.stat().st_mtime)


def friendly_error_message(output: str) -> str:
    lower = output.lower()
    messages: list[str] = []

    if "http error 429" in lower or "too many requests" in lower:
        messages.append("YouTube membatasi request sementara. Coba lagi nanti atau gunakan URL lain.")

    if "requested format is not available" in lower or "format is not available" in lower:
        messages.append("Format tidak tersedia. Coba pilih Best atau kualitas lain.")

    if not messages:
        return output

    return f"{output}\n\n" + "\n".join(messages)


def run_download(
    command: list[str],
    output_dir: Path = DEFAULT_DOWNLOAD_DIR,
    log_callback: LogCallback | None = None,
) -> Path:
    output_dir = ensure_download_dir(output_dir)
    started_at = time.time()

    if log_callback:
        log_callback(f"> {command_to_display(command)}")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=CREATE_NO_WINDOW,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("yt-dlp tidak ditemukan di PATH.") from exc

    output_lines: list[str] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        text = "".join(buffer).strip()
        buffer.clear()
        if not text:
            return
        output_lines.append(text)
        if log_callback:
            log_callback(text)

    if process.stdout:
        while True:
            char = process.stdout.read(1)
            if char == "" and process.poll() is not None:
                break
            if not char:
                continue
            if char in {"\r", "\n"}:
                flush_buffer()
            else:
                buffer.append(char)
        flush_buffer()

    return_code = process.wait()
    if return_code != 0:
        tail = "\n".join(output_lines[-25:]) or "Download gagal."
        raise RuntimeError(friendly_error_message(tail))

    for line in reversed(output_lines):
        candidate = _path_from_line(line, output_dir)
        if candidate and candidate.exists():
            return candidate

    newest = _find_newest_download(output_dir, started_at)
    if newest:
        return newest

    raise RuntimeError("Download selesai, tetapi file hasil tidak ditemukan di folder download.")
