# YT-DLP Command Library

Library ini berisi kumpulan command `yt-dlp` yang akan dipakai sebagai dasar logic aplikasi GUI lokal.

Tujuan file ini:
1. Menjadi referensi command sebelum membuat GUI.
2. Menghindari logic asal-asalan di GUI.
3. Memisahkan mode download dengan jelas:
   - Video + Audio
   - Video Only
   - Audio Only
   - Playlist / Mix
   - Metadata / Analisis
   - Subtitle
   - Thumbnail
   - Debug
4. Menjelaskan command mana yang cocok untuk GUI sederhana.

Catatan penting:
- Gunakan command ini hanya untuk konten yang memang punya hak atau izin untuk diunduh.
- Jangan menambahkan fitur bypass DRM, premium content, login otomatis, cookies otomatis, atau bypass proteksi.
- Di GUI Python, command harus dibuat dalam bentuk list argument, bukan string mentah.
- Di Python subprocess, jangan gunakan `shell=True` kecuali benar-benar perlu.
- Placeholder `"URL"` berarti URL video/playlist.
- Placeholder `"OUTPUT_DIR"` berarti folder output.
- Folder output default project ini:

```text
C:\Users\mlfad\downloads\ytdlp
````

Output template default:

```text
C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s
```

Output template video only:

```text
C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s
```

Output template audio only:

```text
C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s
```

Output template playlist:

```text
C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s
```

---

# 1. Konsep Format Selector yt-dlp

## 1.1 Selector utama

| Selector          | Arti                                                                              | Cocok untuk          |
| ----------------- | --------------------------------------------------------------------------------- | -------------------- |
| `bv`              | Best video-only. Tidak punya audio.                                               | Video Only           |
| `bv*`             | Best format yang mengandung video. Bisa punya audio.                              | Video + Audio        |
| `ba`              | Best audio-only. Tidak punya video.                                               | Audio Only           |
| `b`               | Best combined video + audio dalam satu format.                                    | Fallback             |
| `bv+ba`           | Ambil video-only terbaik dan audio-only terbaik lalu merge.                       | Video + Audio        |
| `bv*+ba/b`        | Ambil format terbaik yang mengandung video + audio terbaik, fallback ke combined. | Video + Audio normal |
| `ba[ext=m4a]/ba`  | Prioritaskan audio m4a, fallback audio terbaik.                                   | Audio Only Original  |
| `ba[ext=opus]/ba` | Prioritaskan audio opus, fallback audio terbaik.                                  | Audio Only Original  |

## 1.2 Aturan penting

Untuk mode Video Only:

```text
Gunakan: bv
Jangan gunakan: bv*
```

Alasan:

* `bv` berarti video-only.
* `bv*` berarti format yang mengandung video, tetapi bisa saja sudah punya audio.

Untuk mode Audio Only:

```text
Gunakan: ba
Jangan gunakan: resolusi video seperti 720p / 360p sebagai kualitas audio.
```

Untuk mode Video + Audio:

```text
Gunakan: bv*+ba/b
```

Alasan:

* Mode ini memang butuh hasil akhir video + audio.
* `bv*+ba/b` cocok untuk download normal karena fallback-nya lebih aman.

---

# 2. Command Cek Dependency

## 2.1 Cek yt-dlp

```powershell
yt-dlp --version
```

Keterangan:

* Dipakai untuk memastikan `yt-dlp` terinstall dan tersedia di PATH.

## 2.2 Cek FFmpeg

```powershell
ffmpeg -version
```

Keterangan:

* Dibutuhkan untuk merge video + audio.
* Dibutuhkan untuk convert audio ke MP3/WAV/M4A.
* Dibutuhkan untuk potong video dengan `--download-sections`.

## 2.3 Cek FFprobe

```powershell
ffprobe -version
```

Keterangan:

* Bisa dipakai untuk memverifikasi hasil akhir:

  * file punya video atau tidak
  * file punya audio atau tidak
  * resolusi file
  * codec video/audio

---

# 3. Command Analisis / Metadata

Bagian ini untuk analisis, bukan download utama.

## 3.1 Lihat semua format yang tersedia

```powershell
yt-dlp -F "URL"
```

Keterangan:

* Menampilkan format_id, resolusi, codec, audio/video, dan kadang ukuran.
* Cocok untuk debugging.
* Tidak cocok dijadikan parser utama di GUI karena output tabel bisa berubah.

## 3.2 Ambil metadata JSON satu URL

```powershell
yt-dlp -J --no-playlist "URL"
```

Keterangan:

* Menghasilkan JSON metadata.
* Cocok untuk advanced mode.
* Bisa dipakai untuk membaca `formats`, `title`, `duration`, `thumbnail`, dan sebagainya.
* Untuk GUI sederhana, ini tidak wajib dijalankan sebelum download.

## 3.3 Ambil metadata JSON per video

```powershell
yt-dlp -j --no-playlist "URL"
```

Keterangan:

* Mirip `-J`, tetapi `-j` menghasilkan JSON untuk setiap video.
* Biasanya lebih berguna untuk pipeline atau script.

## 3.4 Simulasi tanpa download

```powershell
yt-dlp --simulate "URL"
```

Keterangan:

* Mengecek metadata/proses tanpa menyimpan file.

## 3.5 Print judul video

```powershell
yt-dlp --print title --no-playlist "URL"
```

Keterangan:

* Mengambil judul video saja.

## 3.6 Print durasi video

```powershell
yt-dlp --print duration_string --no-playlist "URL"
```

Keterangan:

* Mengambil durasi dalam format mudah dibaca.

## 3.7 Print path final setelah download

```powershell
yt-dlp --print after_move:filepath "URL"
```

Keterangan:

* Berguna untuk GUI agar tahu file akhir tersimpan di mana.
* Bisa digabung dengan command download.
* Untuk GUI, lebih baik tetap tampilkan log real-time juga.

---

# 4. Download Normal Video + Audio

Mode ini adalah mode download biasa seperti video asli: ada video dan audio.

## 4.1 Video + Audio kualitas terbaik

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Cocok untuk tombol `Video + Audio` dengan kualitas `Best`.
* `bv*+ba/b` mengambil format terbaik yang mengandung video + audio terbaik.
* Jika tidak bisa, fallback ke combined format `b`.
* `--merge-output-format "mp4/mkv"` membuat yt-dlp/FFmpeg memilih container merge yang cocok.

## 4.2 Video + Audio maksimal 1080p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:1080,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Cocok untuk kualitas `1080p`.
* `-S "res:1080,fps"` mengurutkan format agar memilih resolusi terbaik yang mendekati/maksimal 1080p, dengan preferensi fps lebih baik.

## 4.3 Video + Audio maksimal 720p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:720,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 4.4 Video + Audio maksimal 480p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:480,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 4.5 Video + Audio maksimal 360p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:360,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 4.6 Video + Audio maksimal 240p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:240,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 4.7 Video + Audio maksimal 144p

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" -S "res:144,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

---

# 5. Download Video + Audio dengan Preferensi MP4

Mode ini lebih cocok jika targetnya file yang mudah diputar di Windows/HP.

## 5.1 Video + Audio MP4 compatible

```powershell
yt-dlp --no-playlist -t mp4 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-t mp4` adalah preset yt-dlp untuk output MP4.
* Cocok untuk GUI jika user ingin mode `MP4 Compatible`.
* Bisa lebih lambat jika perlu remux/recode tergantung format sumber.

## 5.2 Video + Audio MP4 maksimal 720p

```powershell
yt-dlp --no-playlist -t mp4 -S "res:720,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 5.3 Alternatif manual MP4/M4A

```powershell
yt-dlp --no-playlist -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Prioritaskan video MP4 dan audio M4A.
* Jika tidak ada, fallback ke combined MP4.
* Jika masih tidak ada, fallback ke format normal.

---

# 6. Download Video Only

Mode ini menghasilkan file yang hanya punya video, tanpa audio.

## 6.1 Video Only kualitas terbaik

```powershell
yt-dlp --no-playlist -f "bv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Ini command utama untuk mode `Video Only - Best`.
* `bv` wajib dipakai karena artinya video-only.
* Jangan pakai `bv*`.

## 6.2 Video Only maksimal 1080p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:1080,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.3 Video Only maksimal 720p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:720,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.4 Video Only maksimal 480p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:480,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.5 Video Only maksimal 360p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:360,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.6 Video Only maksimal 240p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:240,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.7 Video Only maksimal 144p

```powershell
yt-dlp --no-playlist -f "bv" -S "res:144,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## 6.8 Video Only dengan filter ketat height

```powershell
yt-dlp --no-playlist -f "bv[height<=720]" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Ini lebih ketat, tetapi bisa gagal jika format tidak tersedia.
* Untuk GUI sederhana, lebih aman pakai `-f "bv" -S "res:720,fps"`.

---

# 7. Download Audio Only Original

Mode ini mengambil audio asli terbaik tanpa convert ke MP3.

## 7.1 Audio Only original terbaik

```powershell
yt-dlp --no-playlist -f "ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Ini command utama untuk `Audio Only Original - Best`.
* Tidak mengubah format audio.
* Hasil bisa `.m4a`, `.webm`, `.opus`, atau format lain tergantung sumber.

## 7.2 Audio Only prefer M4A

```powershell
yt-dlp --no-playlist -f "ba[ext=m4a]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Prioritaskan M4A.
* Jika M4A tidak tersedia, fallback ke audio terbaik.

## 7.3 Audio Only prefer OPUS

```powershell
yt-dlp --no-playlist -f "ba[ext=opus]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Prioritaskan OPUS.
* Jika OPUS tidak tersedia, fallback ke audio terbaik.

## 7.4 Audio Only prefer WEBM

```powershell
yt-dlp --no-playlist -f "ba[ext=webm]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

---

# 8. Download Audio Only Convert

Mode ini mengambil audio lalu mengubahnya ke format tertentu. Butuh FFmpeg.

## 8.1 Audio Only MP3 kualitas terbaik VBR

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-x` berarti extract audio.
* `--audio-format mp3` berarti output MP3.
* `--audio-quality 0` berarti kualitas VBR terbaik.

## 8.2 Audio Only MP3 320K

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 320K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.3 Audio Only MP3 256K

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 256K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.4 Audio Only MP3 192K

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 192K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.5 Audio Only MP3 128K

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 128K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.6 Audio Only M4A

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format m4a -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.7 Audio Only WAV

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format wav -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 8.8 Audio Only FLAC

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format flac -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

---

# 9. Download Playlist / Mix

## 9.1 Download hanya video, jangan playlist

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `--no-playlist` membuat yt-dlp hanya download video tersebut jika URL mengandung parameter playlist.

## 9.2 Download playlist / mix

```powershell
yt-dlp --yes-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `--yes-playlist` membuat yt-dlp mengunduh playlist jika URL memang playlist.
* Cocok untuk mode `Playlist / Mix`.

## 9.3 Download playlist maksimal 720p

```powershell
yt-dlp --yes-playlist -f "bv*+ba/b" -S "res:720,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

## 9.4 Download hanya item tertentu dari playlist

```powershell
yt-dlp --yes-playlist -I 1:5 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-I 1:5` berarti download item playlist nomor 1 sampai 5.

## 9.5 Download satu item tertentu dari playlist

```powershell
yt-dlp --yes-playlist -I 3 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-I 3` berarti download item playlist nomor 3.

## 9.6 Download playlist tetapi batasi jumlah file

```powershell
yt-dlp --yes-playlist --max-downloads 10 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

## 9.7 Download playlist dengan archive agar tidak download ulang

```powershell
yt-dlp --yes-playlist --download-archive "C:\Users\mlfad\downloads\ytdlp\archive.txt" -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `--download-archive` menyimpan ID video yang sudah diunduh.
* Cocok untuk playlist/channel yang akan diunduh bertahap.

---

# 10. Batch Download dari File URL

## 10.1 Download banyak URL dari file

```powershell
yt-dlp -a "urls.txt" -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s"
```

Keterangan:

* File `urls.txt` berisi satu URL per baris.
* Cocok untuk mode batch sederhana.

## 10.2 Batch audio MP3

```powershell
yt-dlp -a "urls.txt" -f "ba" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s"
```

---

# 11. Subtitle

## 11.1 Lihat subtitle yang tersedia

```powershell
yt-dlp --list-subs --no-playlist "URL"
```

## 11.2 Download subtitle manual

```powershell
yt-dlp --no-playlist --write-subs --sub-langs "id,en" --skip-download -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 11.3 Download auto subtitle

```powershell
yt-dlp --no-playlist --write-auto-subs --sub-langs "id,en" --skip-download -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 11.4 Download video + embed subtitle

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --write-subs --sub-langs "id,en" --embed-subs -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Embed subtitle hanya berlaku pada format/container yang mendukung.
* Kalau gagal embed, subtitle bisa tetap terunduh sebagai file terpisah.

---

# 12. Thumbnail dan Metadata

## 12.1 Download thumbnail saja

```powershell
yt-dlp --no-playlist --write-thumbnail --skip-download -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 12.2 Download video + thumbnail

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --write-thumbnail -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 12.3 Download video + embed metadata

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --embed-metadata -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 12.4 Audio MP3 + metadata

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 --embed-metadata -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

---

# 13. Potong Video / Audio Berdasarkan Waktu

Butuh FFmpeg.

## 13.1 Download potongan video dari menit 01:00 sampai 02:30

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --download-sections "*00:01:00-00:02:30" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s CUT [%(id)s].%(ext)s" "URL"
```

## 13.2 Download dari detik 10 sampai selesai

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --download-sections "*00:00:10-inf" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s CUT [%(id)s].%(ext)s" "URL"
```

## 13.3 Download potongan audio MP3

```powershell
yt-dlp --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 --download-sections "*00:01:00-00:02:30" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s CUT [%(id)s].%(ext)s" "URL"
```

---

# 14. Naming dan File Safety

## 14.1 Batasi panjang nama file

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --trim-filenames 120 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 14.2 Nama file lebih aman untuk Windows

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --windows-filenames -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 14.3 Nama file ASCII sederhana

```powershell
yt-dlp --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" --restrict-filenames -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `--restrict-filenames` membuat nama file lebih aman tapi bisa mengubah karakter non-ASCII.

---

# 15. Progress dan Log untuk GUI

## 15.1 Output progress per baris

```powershell
yt-dlp --newline --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `--newline` membuat progress lebih mudah dibaca realtime oleh GUI.

## 15.2 Print path file akhir setelah download

```powershell
yt-dlp --newline --print after_move:filepath --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Cocok untuk GUI agar bisa menampilkan lokasi file hasil.

## 15.3 Template progress custom

```powershell
yt-dlp --newline --progress-template "download:%(progress._percent_str)s %(progress._speed_str)s ETA %(progress._eta_str)s" --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Berguna jika GUI ingin parsing progress.
* Untuk GUI sederhana, cukup tampilkan log mentah dulu.

---

# 16. Speed, Retry, dan Stabilitas

## 16.1 Download fragment paralel

```powershell
yt-dlp --no-playlist -N 4 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-N 4` mengunduh fragment secara paralel.
* Bisa mempercepat beberapa video, tapi tidak selalu.

## 16.2 Batasi kecepatan download

```powershell
yt-dlp --no-playlist -r 2M -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* `-r 2M` membatasi speed sekitar 2 MB/s.

## 16.3 Retry lebih banyak

```powershell
yt-dlp --no-playlist -R 20 --fragment-retries 20 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## 16.4 Tambahkan jeda antar request

```powershell
yt-dlp --no-playlist --sleep-requests 1 --sleep-interval 3 --max-sleep-interval 8 -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Keterangan:

* Bisa membantu mengurangi request terlalu agresif.
* Tidak menjamin mengatasi HTTP 429.

---

# 17. Debug

## 17.1 Debug verbose

```powershell
yt-dlp -v --no-playlist "URL"
```

## 17.2 Debug verbose + update check

```powershell
yt-dlp -vU --no-playlist "URL"
```

Keterangan:

* Berguna saat mau melaporkan bug atau membaca penyebab error.

## 17.3 Update yt-dlp jika install binary resmi

```powershell
yt-dlp -U
```

## 17.4 Update yt-dlp jika install via winget

```powershell
winget upgrade yt-dlp
```

---

# 18. Mapping Mode GUI Sederhana

Bagian ini yang sebaiknya dipakai untuk `command_builder.py`.

## 18.1 Mode: Video + Audio

Quality options:

```text
Best
1080p
720p
480p
360p
240p
144p
```

Command Best:

```powershell
yt-dlp --newline --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Command quality tertentu:

```powershell
yt-dlp --newline --no-playlist -f "bv*+ba/b" -S "res:720,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Catatan:

* Ganti `720` sesuai pilihan quality.
* Untuk Video + Audio, `bv*` boleh dipakai.

## 18.2 Mode: Video Only

Quality options:

```text
Best
1080p
720p
480p
360p
240p
144p
```

Command Best:

```powershell
yt-dlp --newline --no-playlist -f "bv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

Command quality tertentu:

```powershell
yt-dlp --newline --no-playlist -f "bv" -S "res:720,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

Catatan:

* Ganti `720` sesuai pilihan quality.
* Untuk Video Only, jangan pernah pakai `bv*`.

## 18.3 Mode: Audio Only MP3

Quality options:

```text
Best VBR
320K
256K
192K
128K
```

Command Best VBR:

```powershell
yt-dlp --newline --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Command bitrate tertentu:

```powershell
yt-dlp --newline --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 192K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

Catatan:

* Ganti `192K` sesuai pilihan quality.
* Jangan tampilkan 1080p/720p/360p di mode audio.

## 18.4 Mode: Audio Only Original

Quality options:

```text
Best
M4A Preferred
OPUS Preferred
WEBM Preferred
```

Command Best:

```powershell
yt-dlp --newline --no-playlist -f "ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Command M4A Preferred:

```powershell
yt-dlp --newline --no-playlist -f "ba[ext=m4a]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Command OPUS Preferred:

```powershell
yt-dlp --newline --no-playlist -f "ba[ext=opus]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

Command WEBM Preferred:

```powershell
yt-dlp --newline --no-playlist -f "ba[ext=webm]/ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

---

# 19. Mapping Playlist GUI

Jika GUI nanti menambah mode playlist, jangan campur dengan mode single video.

## 19.1 Playlist Video + Audio

Quality options:

```text
Best
1080p
720p
480p
360p
240p
144p
```

Command Best:

```powershell
yt-dlp --newline --yes-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

Command quality tertentu:

```powershell
yt-dlp --newline --yes-playlist -f "bv*+ba/b" -S "res:720,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

## 19.2 Playlist Audio MP3

```powershell
yt-dlp --newline --yes-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

## 19.3 Playlist Audio Original

```powershell
yt-dlp --newline --yes-playlist -f "ba" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

---

# 20. Command Builder Pseudocode

Pseudocode ini untuk programmer/Codex.

```python
def build_ytdlp_command(url: str, mode: str, quality: str, output_dir: str) -> list[str]:
    base = [
        "yt-dlp",
        "--newline",
        "--no-playlist",
    ]

    normal_template = f"{output_dir}\\%(title).120s [%(id)s].%(ext)s"
    video_only_template = f"{output_dir}\\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s"
    audio_only_template = f"{output_dir}\\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s"

    if mode == "Video + Audio":
        cmd = base + ["-f", "bv*+ba/b"]

        if quality != "Best":
            resolution = quality.replace("p", "")
            cmd += ["-S", f"res:{resolution},fps"]

        cmd += [
            "--merge-output-format", "mp4/mkv",
            "-o", normal_template,
            url,
        ]
        return cmd

    if mode == "Video Only":
        cmd = base + ["-f", "bv"]

        if quality != "Best":
            resolution = quality.replace("p", "")
            cmd += ["-S", f"res:{resolution},fps"]

        cmd += [
            "-o", video_only_template,
            url,
        ]
        return cmd

    if mode == "Audio Only MP3":
        audio_quality = "0" if quality == "Best VBR" else quality

        cmd = base + [
            "-f", "ba",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", audio_quality,
            "-o", normal_template,
            url,
        ]
        return cmd

    if mode == "Audio Only Original":
        if quality == "M4A Preferred":
            selector = "ba[ext=m4a]/ba"
        elif quality == "OPUS Preferred":
            selector = "ba[ext=opus]/ba"
        elif quality == "WEBM Preferred":
            selector = "ba[ext=webm]/ba"
        else:
            selector = "ba"

        cmd = base + [
            "-f", selector,
            "-o", audio_only_template,
            url,
        ]
        return cmd

    raise ValueError("Mode tidak valid")
```

Catatan:

* Pseudocode ini tidak memakai `shell=True`.
* Command dikembalikan sebagai list.
* Kualitas audio dan kualitas video dipisahkan.
* Audio mode tidak pernah memakai `res`.
* Video Only tidak pernah memakai `bv*`.

---

# 21. UI Logic yang Benar

## 21.1 Mode Video + Audio

Jika mode dipilih:

```text
Video + Audio
```

Quality dropdown harus berisi:

```text
Best
1080p
720p
480p
360p
240p
144p
```

## 21.2 Mode Video Only

Jika mode dipilih:

```text
Video Only
```

Quality dropdown harus berisi:

```text
Best
1080p
720p
480p
360p
240p
144p
```

## 21.3 Mode Audio Only MP3

Jika mode dipilih:

```text
Audio Only MP3
```

Quality dropdown harus berisi:

```text
Best VBR
320K
256K
192K
128K
```

Tidak boleh ada:

```text
1080p
720p
480p
360p
240p
144p
```

## 21.4 Mode Audio Only Original

Jika mode dipilih:

```text
Audio Only Original
```

Quality dropdown harus berisi:

```text
Best
M4A Preferred
OPUS Preferred
WEBM Preferred
```

Tidak boleh ada:

```text
1080p
720p
480p
360p
240p
144p
```

---

# 22. Error Message Mapping untuk GUI

## 22.1 URL kosong

Pesan:

```text
URL belum diisi.
```

## 22.2 yt-dlp tidak ditemukan

Pesan:

```text
yt-dlp tidak ditemukan. Pastikan yt-dlp sudah terinstall dan tersedia di PATH.
```

## 22.3 FFmpeg tidak ditemukan

Untuk Video + Audio:

```text
FFmpeg tidak ditemukan. Merge video + audio bisa gagal.
```

Untuk Audio Only MP3:

```text
FFmpeg tidak ditemukan. Convert ke MP3 bisa gagal.
```

## 22.4 Requested format is not available

Pesan:

```text
Format tidak tersedia. Coba pilih Best atau kualitas lain.
```

## 22.5 HTTP Error 429

Pesan:

```text
YouTube sedang membatasi request sementara. Coba lagi nanti, gunakan URL lain, atau kurangi percobaan berulang.
```

## 22.6 Download selesai

Pesan:

```text
Download selesai. Cek folder output.
```

---

# 23. Rekomendasi Fitur GUI Minimal

GUI sebaiknya hanya punya:

1. Input URL.
2. Dropdown Mode.
3. Dropdown Quality yang berubah sesuai Mode.
4. Tombol Download.
5. Tombol Open Downloads Folder.
6. Tombol Clear Log.
7. Label status dependency:

   * yt-dlp: OK/Missing
   * ffmpeg: OK/Missing
   * ffprobe: OK/Missing
8. Area log realtime.

Jangan tampilkan di UI utama:

1. Tabel format.
2. format_id.
3. vcodec.
4. acodec.
5. tbr/vbr/abr.
6. Metadata panjang.
7. Analyze dashboard.
8. Advanced format picker.

Kalau nanti mau advanced mode, buat terpisah. Jangan gabungkan dengan UI utama.

---

# 24. Command Paling Penting untuk Project Ini

## Video + Audio Best

```powershell
yt-dlp --newline --no-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## Video + Audio 720p

```powershell
yt-dlp --newline --no-playlist -f "bv*+ba/b" -S "res:720,fps" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## Video Only Best

```powershell
yt-dlp --newline --no-playlist -f "bv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## Video Only 720p

```powershell
yt-dlp --newline --no-playlist -f "bv" -S "res:720,fps" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"
```

## Audio Only MP3 Best

```powershell
yt-dlp --newline --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## Audio Only MP3 192K

```powershell
yt-dlp --newline --no-playlist -f "ba" -x --audio-format mp3 --audio-quality 192K -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"
```

## Audio Only Original Best

```powershell
yt-dlp --newline --no-playlist -f "ba" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"
```

## Playlist Video + Audio Best

```powershell
yt-dlp --newline --yes-playlist -f "bv*+ba/b" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(playlist_title).120s\%(playlist_index)03d - %(title).120s [%(id)s].%(ext)s" "URL"
```

---

# 25. Prinsip Akhir

Sebelum membuat GUI, pastikan command builder benar.

Aplikasi GUI tidak perlu pintar berlebihan. GUI cukup:

1. Membaca pilihan user.
2. Membangun command yang benar.
3. Menjalankan yt-dlp.
4. Menampilkan log.
5. Menyimpan file ke folder output.

Jika command library ini sudah benar, GUI akan lebih mudah dibuat dan lebih kecil kemungkinan bug.

```

Untuk GUI-mu, ambil dulu hanya bagian `18`, `21`, `22`, dan `24`. Jangan implement semua isi library sekaligus. Kalau semua fitur dimasukkan, nanti balik lagi jadi aplikasi gemuk dan rusak.
::contentReference[oaicite:1]{index=1}
```

