from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from . import command_builder, ytdlp_client


class DependencyWorker(QThread):
    result = Signal(dict)
    log = Signal(str)

    def run(self) -> None:
        self.log.emit("Checking dependencies...")
        self.result.emit(ytdlp_client.check_dependencies())


class DownloadWorker(QThread):
    log = Signal(str)
    success = Signal(str)
    failure = Signal(str)

    def __init__(self, command: list[str], output_dir: Path) -> None:
        super().__init__()
        self.command = command
        self.output_dir = output_dir

    def run(self) -> None:
        try:
            output_path = ytdlp_client.run_download(self.command, self.output_dir, self.log.emit)
        except Exception as exc:  # noqa: BLE001 - error is shown in the GUI.
            self.failure.emit(str(exc))
            return
        self.success.emit(str(output_path))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("YT-DLP GUI Local")
        self.resize(760, 560)

        self.download_dir = ytdlp_client.DEFAULT_DOWNLOAD_DIR
        self.dependencies: dict[str, dict[str, Any]] = {}
        self.folder_ready = False
        self.dependency_worker: DependencyWorker | None = None
        self.download_worker: DownloadWorker | None = None

        self._build_ui()
        self._apply_theme()
        self._prepare_download_folder()
        self.set_status("Ready")
        self._start_dependency_check()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(12)

        title = QLabel("YT-DLP GUI Local")
        title.setObjectName("Title")
        note = QLabel("Gunakan hanya untuk konten yang memang Anda punya hak atau izin untuk unduh.")
        note.setObjectName("Note")
        note.setWordWrap(True)
        root.addWidget(title)
        root.addWidget(note)

        dependency_group = QGroupBox("Dependency")
        dependency_layout = QGridLayout(dependency_group)
        self.ytdlp_label = QLabel("yt-dlp: Checking")
        self.ffmpeg_label = QLabel("ffmpeg: Checking")
        self.ffprobe_label = QLabel("ffprobe: Checking")
        dependency_layout.addWidget(self.ytdlp_label, 0, 0)
        dependency_layout.addWidget(self.ffmpeg_label, 0, 1)
        dependency_layout.addWidget(self.ffprobe_label, 0, 2)
        root.addWidget(dependency_group)

        form_group = QGroupBox("Download")
        form = QFormLayout(form_group)
        form.setLabelAlignment(Qt.AlignLeft)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste URL YouTube di sini")

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(command_builder.MODE_OPTIONS)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)

        self.quality_combo = QComboBox()

        form.addRow("URL", self.url_input)
        form.addRow("Mode", self.mode_combo)
        form.addRow("Kualitas", self.quality_combo)
        root.addWidget(form_group)

        button_row = QHBoxLayout()
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setEnabled(False)
        self.open_folder_button = QPushButton("Open Downloads Folder")
        self.open_folder_button.clicked.connect(self.open_download_folder)
        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.clear_log)
        button_row.addWidget(self.download_button)
        button_row.addWidget(self.open_folder_button)
        button_row.addWidget(self.clear_log_button)
        button_row.addStretch(1)
        root.addLayout(button_row)

        status_row = QHBoxLayout()
        status_title = QLabel("Status akhir:")
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("Status")
        status_row.addWidget(status_title)
        status_row.addWidget(self.status_label, 1)
        root.addLayout(status_row)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        root.addWidget(self.result_label)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Progress dan log yt-dlp akan muncul di sini.")
        root.addWidget(self.log_area, 1)

        self.on_mode_changed(self.mode_combo.currentText())

    def _apply_theme(self) -> None:
        QApplication.setStyle("Fusion")
        self.setStyleSheet(
            """
            QWidget {
                background: #17191d;
                color: #edf0f5;
                font-size: 13px;
            }
            QLabel#Title {
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#Note {
                color: #aeb6c2;
            }
            QLabel#Status {
                font-weight: 700;
            }
            QGroupBox {
                border: 1px solid #303642;
                border-radius: 6px;
                margin-top: 10px;
                padding: 10px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QLineEdit, QComboBox, QTextEdit {
                background: #0f1115;
                border: 1px solid #303642;
                border-radius: 5px;
                color: #f3f5f8;
                selection-background-color: #315b8f;
                selection-color: #ffffff;
            }
            QLineEdit, QComboBox {
                padding: 7px;
            }
            QTextEdit {
                padding: 8px;
                font-family: Consolas, "Courier New", monospace;
                font-size: 12px;
            }
            QPushButton {
                background: #2f6fb3;
                border: 1px solid #3f82ca;
                border-radius: 5px;
                padding: 8px 14px;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #377fca;
            }
            QPushButton:disabled {
                background: #2a2f38;
                border-color: #363c46;
                color: #7e8794;
            }
            """
        )

    def _prepare_download_folder(self) -> None:
        try:
            ytdlp_client.ensure_download_dir(self.download_dir)
        except Exception as exc:  # noqa: BLE001 - surfaced in GUI.
            self.folder_ready = False
            self.append_log(str(exc))
            self.set_status("Failed", str(exc), is_error=True)
            self.open_folder_button.setEnabled(False)
            return

        self.folder_ready = True
        self.append_log(f"Download folder: {self.download_dir}")

    def _start_dependency_check(self) -> None:
        self.dependency_worker = DependencyWorker()
        self.dependency_worker.log.connect(self.append_log)
        self.dependency_worker.result.connect(self.on_dependency_result)
        self.dependency_worker.start()

    def on_dependency_result(self, result: dict[str, Any]) -> None:
        self.dependencies = result
        self._set_dependency_status(self.ytdlp_label, "yt-dlp", result.get("yt-dlp", {}))
        self._set_dependency_status(self.ffmpeg_label, "ffmpeg", result.get("ffmpeg", {}))
        self._set_dependency_status(self.ffprobe_label, "ffprobe", result.get("ffprobe", {}))

        if not result.get("yt-dlp", {}).get("available"):
            self.download_button.setEnabled(False)
            self.set_status("Failed", "yt-dlp tidak ditemukan. Install yt-dlp atau tambahkan ke PATH.", True)
            return

        self.download_button.setEnabled(self.folder_ready)
        self.set_status("Ready", "Siap download.")

        if not result.get("ffmpeg", {}).get("available"):
            self.append_log("Warning: ffmpeg Missing. Merge video+audio atau convert MP3 bisa gagal.")
        if not result.get("ffprobe", {}).get("available"):
            self.append_log("Info: ffprobe Missing. Aplikasi tetap bisa download tanpa verifikasi detail.")

    def _set_dependency_status(self, label: QLabel, name: str, status: dict[str, Any]) -> None:
        if status.get("available"):
            label.setText(f"{name}: OK")
            label.setStyleSheet("color: #8fe18f;")
        else:
            label.setText(f"{name}: Missing")
            label.setStyleSheet("color: #ffb86b;")

    def on_mode_changed(self, _mode: str) -> None:
        mode = self.mode_combo.currentText()
        current = self.quality_combo.currentText()
        qualities = command_builder.qualities_for_mode(mode)

        self.quality_combo.blockSignals(True)
        self.quality_combo.clear()
        self.quality_combo.addItems(qualities)
        if current in qualities:
            self.quality_combo.setCurrentText(current)
        self.quality_combo.blockSignals(False)

    def start_download(self) -> None:
        url = self.url_input.text().strip()
        if not url:
            self.set_status("Failed", "URL kosong. Paste URL terlebih dahulu.", True)
            return
        if not self._looks_like_url(url):
            self.set_status("Failed", "URL tidak valid. Gunakan URL http atau https.", True)
            return
        if not self.folder_ready:
            self.set_status("Failed", f"Folder download tidak siap: {self.download_dir}", True)
            return
        if not self.dependencies.get("yt-dlp", {}).get("available"):
            self.set_status("Failed", "yt-dlp tidak ditemukan. Download tidak bisa berjalan.", True)
            return

        mode = self.mode_combo.currentText()
        quality = self.quality_combo.currentText()

        if mode == command_builder.MODE_VIDEO_AUDIO and not self.dependencies.get("ffmpeg", {}).get("available"):
            self.append_log("Warning: ffmpeg Missing. Merge video+audio bisa gagal.")
        if mode == command_builder.MODE_AUDIO_MP3 and not self.dependencies.get("ffmpeg", {}).get("available"):
            self.append_log("Warning: ffmpeg Missing. Convert MP3 bisa gagal.")

        try:
            command = command_builder.build_ytdlp_command(url, mode, quality, self.download_dir)
        except Exception as exc:  # noqa: BLE001 - surfaced in GUI.
            self.set_status("Failed", str(exc), True)
            return

        self.download_button.setEnabled(False)
        self.set_status("Downloading", f"Mode: {mode} | Kualitas: {quality}")
        self.append_log("")
        self.append_log(f"Starting download: {mode} / {quality}")

        self.download_worker = DownloadWorker(command, self.download_dir)
        self.download_worker.log.connect(self.append_log)
        self.download_worker.success.connect(self.on_download_success)
        self.download_worker.failure.connect(self.on_download_failure)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.start()

    def on_download_success(self, file_path: str) -> None:
        self.set_status("Finished", f"File selesai: {file_path}")
        self.append_log(f"Finished: {file_path}")

    def on_download_failure(self, message: str) -> None:
        self.set_status("Failed", message, True)
        self.append_log(f"Failed: {message}")

    def on_download_finished(self) -> None:
        if self.dependencies.get("yt-dlp", {}).get("available") and self.folder_ready:
            self.download_button.setEnabled(True)

    def open_download_folder(self) -> None:
        try:
            ytdlp_client.ensure_download_dir(self.download_dir)
        except Exception as exc:  # noqa: BLE001 - surfaced in GUI.
            self.set_status("Failed", str(exc), True)
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.download_dir)))

    def clear_log(self) -> None:
        self.log_area.clear()

    def append_log(self, message: str) -> None:
        self.log_area.append(message)
        self.log_area.moveCursor(QTextCursor.MoveOperation.End)

    def set_status(self, status: str, detail: str = "", is_error: bool = False) -> None:
        self.status_label.setText(status)
        self.status_label.setStyleSheet("color: #ff9b9b;" if is_error else "color: #aee9b1;")
        self.result_label.setText(detail)
        self.result_label.setStyleSheet("color: #ffb1b1;" if is_error else "color: #c9d2df;")

    @staticmethod
    def _looks_like_url(value: str) -> bool:
        return bool(re.match(r"^https?://\S+$", value, flags=re.IGNORECASE))
