# YT-DLP GUI Local

Aplikasi desktop GUI lokal sederhana untuk menjalankan `yt-dlp` di Windows. Aplikasi ini dibuat dengan Python + PySide6, berjalan sebagai window desktop biasa, dan bukan web app, browser app, server lokal, Electron, atau aplikasi online.

## Fitur

- Paste URL, pilih mode, pilih kualitas, lalu klik Download.
- Log `yt-dlp` tampil realtime dan UI tidak freeze saat download.
- Folder download dibuat otomatis.
- Dependency dicek saat aplikasi dibuka.

## Dependency

Dibutuhkan:

- Python 3
- yt-dlp
- ffmpeg
- ffprobe

Aplikasi mengecek ringkas:

- `yt-dlp --version`
- `ffmpeg -version`
- `ffprobe -version`

## Install

```powershell
pip install -r requirements.txt
```

Pastikan `yt-dlp`, `ffmpeg`, dan `ffprobe` tersedia di PATH Windows.

## Menjalankan Aplikasi

```powershell
python main.py
```

## Folder Download

Hasil download disimpan ke:

```text
C:\Users\mlfad\downloads\ytdlp
```

## Mode

- `Video + Audio`: download video dengan audio. Mode ini memakai selector `bv*+ba/b`; kualitas tertentu memakai `-S res:ANGKA,fps`.
- `Video Only`: download video tanpa audio memakai selector `bv`; kualitas tertentu memakai `-S res:ANGKA,fps`. Mode ini tidak memakai `bv*`.
- `Audio Only MP3`: download audio terbaik lalu convert ke MP3. Pilihan kualitasnya adalah `Best VBR`, `320K`, `256K`, `192K`, dan `128K`.
- `Audio Only Original`: download audio terbaik dalam format asli, atau preferensi `m4a`/`opus`.

Jika kualitas tertentu tidak tersedia, pilih `Best` atau kualitas lain.

## Catatan

Gunakan hanya untuk konten yang memang Anda punya hak atau izin untuk unduh. Aplikasi ini berjalan sepenuhnya lokal dan tidak menyediakan fitur login, cookies otomatis, database, atau bypass proteksi konten.
