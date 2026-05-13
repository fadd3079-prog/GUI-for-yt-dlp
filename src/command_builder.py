from __future__ import annotations

from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(r"C:\Users\mlfad\downloads\ytdlp")

MODE_VIDEO_AUDIO = "Video + Audio"
MODE_VIDEO_ONLY = "Video Only"
MODE_AUDIO_MP3 = "Audio Only MP3"
MODE_AUDIO_ORIGINAL = "Audio Only Original"

VIDEO_QUALITIES = ["Best", "1080p", "720p", "480p", "360p", "240p", "144p"]
AUDIO_MP3_QUALITIES = ["Best VBR", "320K", "256K", "192K", "128K"]
AUDIO_ORIGINAL_QUALITIES = ["Best", "M4A Preferred", "OPUS Preferred", "WEBM Preferred"]

MODE_OPTIONS = [
    MODE_VIDEO_AUDIO,
    MODE_VIDEO_ONLY,
    MODE_AUDIO_MP3,
    MODE_AUDIO_ORIGINAL,
]

QUALITY_OPTIONS_BY_MODE = {
    MODE_VIDEO_AUDIO: VIDEO_QUALITIES,
    MODE_VIDEO_ONLY: VIDEO_QUALITIES,
    MODE_AUDIO_MP3: AUDIO_MP3_QUALITIES,
    MODE_AUDIO_ORIGINAL: AUDIO_ORIGINAL_QUALITIES,
}


def qualities_for_mode(mode: str) -> list[str]:
    return list(QUALITY_OPTIONS_BY_MODE.get(mode, VIDEO_QUALITIES))


def _video_resolution(quality: str) -> str | None:
    if quality == "Best":
        return None
    if quality.endswith("p") and quality[:-1].isdigit():
        return quality[:-1]
    raise ValueError(f"Kualitas video tidak dikenal: {quality}")


def _output_template(output_dir: Path, suffix: str = "") -> str:
    suffix_part = f" {suffix}" if suffix else ""
    return str(output_dir / f"%(title).120s{suffix_part} [%(id)s].%(ext)s")


def build_ytdlp_command(url: str, mode: str, quality: str, output_dir: Path) -> list[str]:
    if not url.strip():
        raise ValueError("URL belum diisi.")

    output_dir = Path(output_dir)
    base = ["yt-dlp", "--newline", "--no-playlist"]

    if mode == MODE_VIDEO_AUDIO:
        command = [
            *base,
            "-f",
            "bv*+ba/b",
        ]
        resolution = _video_resolution(quality)
        if resolution is not None:
            command.extend(["-S", f"res:{resolution},fps"])
        command.extend(
            [
                "--merge-output-format",
                "mp4/mkv",
                "-o",
                _output_template(output_dir),
                url,
            ]
        )
        return command

    if mode == MODE_VIDEO_ONLY:
        command = [
            *base,
            "-f",
            "bv",
        ]
        resolution = _video_resolution(quality)
        if resolution is not None:
            command.extend(["-S", f"res:{resolution},fps"])
        command.extend(["-o", _output_template(output_dir, "VIDEO_ONLY"), url])
        return command

    if mode == MODE_AUDIO_MP3:
        audio_quality = "0" if quality == "Best VBR" else quality
        if audio_quality not in {"0", "320K", "256K", "192K", "128K"}:
            raise ValueError(f"Kualitas audio MP3 tidak dikenal: {quality}")
        return [
            *base,
            "-f",
            "ba",
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            audio_quality,
            "-o",
            _output_template(output_dir),
            url,
        ]

    if mode == MODE_AUDIO_ORIGINAL:
        selectors = {
            "Best": "ba",
            "M4A Preferred": "ba[ext=m4a]/ba",
            "OPUS Preferred": "ba[ext=opus]/ba",
            "WEBM Preferred": "ba[ext=webm]/ba",
        }
        selector = selectors.get(quality)
        if selector is None:
            raise ValueError(f"Kualitas audio original tidak dikenal: {quality}")
        return [
            *base,
            "-f",
            selector,
            "-o",
            _output_template(output_dir, "AUDIO_ONLY"),
            url,
        ]

    raise ValueError(f"Mode download tidak dikenal: {mode}")
