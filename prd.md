# PRD - YT-DLP Desktop GUI Lokal

## 1. Ringkasan Project

Project ini adalah aplikasi desktop GUI lokal untuk `yt-dlp` di Windows. Aplikasi berjalan sebagai window desktop biasa, bukan web, bukan browser, bukan server lokal, dan bukan aplikasi online.

Aplikasi dibuat untuk memudahkan penggunaan `yt-dlp` tanpa perlu mengetik command manual di terminal. Fokus utama aplikasi ini bukan tampilan yang terlalu mewah, tetapi akurasi dalam membaca format video/audio asli dari `yt-dlp`.

Direktori project:

`C:\Users\mlfad\ytdlp`

Lokasi default hasil download:

`C:\Users\mlfad\downloads\ytdlp`

Aplikasi harus membuat folder download otomatis jika folder tersebut belum ada.

## 2. Latar Belakang Masalah

Sebelumnya sudah dibuat GUI sederhana, tetapi hasilnya tidak akurat. Masalah yang muncul:

1. Mode Video Only masih bisa menghasilkan file yang punya audio.
2. Resolusi yang dipilih di GUI tidak selalu sama dengan hasil download.
3. Pilihan resolusi dibuat secara statis, misalnya 144p, 240p, 360p, 720p, padahal format yang tersedia di setiap video bisa berbeda.
4. Pemilihan format memakai selector ambigu seperti `bv*`, sehingga masih bisa mengambil format yang mengandung audio.
5. GUI belum membaca format asli dari JSON `yt-dlp`.

Kesalahan utama bukan pada `yt-dlp`, tetapi pada cara GUI memilih format. GUI yang akurat harus membaca data asli dari `yt-dlp -J`, lalu memilih berdasarkan `format_id`, `vcodec`, dan `acodec`.

## 3. Tujuan Project

Tujuan project ini adalah membuat aplikasi GUI lokal yang:

1. Bisa menganalisis URL video menggunakan `yt-dlp`.
2. Menampilkan daftar format asli dari JSON `yt-dlp`.
3. Memisahkan format menjadi:

   * video only
   * audio only
   * combined video + audio
4. Memungkinkan user memilih format berdasarkan data asli yang tersedia.
5. Bisa download:

   * video + audio
   * video only
   * audio only
6. Bisa menampilkan estimasi ukuran file berdasarkan `filesize` atau `filesize_approx`.
7. Bisa menampilkan log download secara realtime.
8. Bisa memverifikasi hasil download dengan `ffprobe` jika tersedia.
9. Menyimpan file ke folder default `C:\Users\mlfad\downloads\ytdlp`.
10. Tetap berjalan sepenuhnya lokal di komputer user.

## 4. Batasan Project

Aplikasi ini tidak boleh dibuat sebagai:

1. Web app.
2. Browser app.
3. Server lokal berbasis FastAPI/Flask.
4. React app.
5. Next.js app.
6. Electron app.
7. Aplikasi online.
8. Aplikasi publik.
9. Aplikasi dengan database.
10. Aplikasi login YouTube.

Aplikasi juga tidak boleh menambahkan fitur:

1. Bypass DRM.
2. Bypass premium content.
3. Bypass konten berbayar.
4. Auto cookies browser.
5. Login akun YouTube.
6. Penyimpanan credential.
7. Pengambilan credential.
8. Fitur untuk mengakali proteksi layanan.

Aplikasi hanya digunakan sebagai GUI lokal untuk menjalankan `yt-dlp` dengan cara yang lebih nyaman dan akurat.

## 5. Tech Stack

Gunakan:

1. Python 3.
2. PySide6 untuk GUI desktop.
3. subprocess untuk menjalankan `yt-dlp`, `ffmpeg`, dan `ffprobe`.
4. QThread atau threading agar UI tidak freeze.
5. JSON parser bawaan Python.
6. pathlib/os untuk path folder dan file.

Jangan gunakan:

1. FastAPI.
2. Flask.
3. Django.
4. React.
5. Next.js.
6. Electron.
7. Database.
8. Browser UI.
9. Web server.

## 6. Struktur Folder

Struktur folder project yang diharapkan:

`C:\Users\mlfad\ytdlp`

* `main.py`
* `requirements.txt`
* `README.md`
* `prd.md`
* `src\__init__.py`
* `src\gui.py`
* `src\ytdlp_client.py`
* `src\format_utils.py`
* `src\ffprobe_utils.py`

Folder hasil download default berada di luar folder project:

`C:\Users\mlfad\downloads\ytdlp`

Aplikasi harus membuat folder tersebut otomatis jika belum ada.

## 7. Peran Setiap File

`main.py`

File utama untuk menjalankan aplikasi. File ini memanggil GUI utama dari `src/gui.py`.

`src/gui.py`

Berisi semua tampilan aplikasi PySide6, layout, tombol, tabel format, area log, status proses, dan event handler.

`src/ytdlp_client.py`

Berisi fungsi untuk:

1. Mengecek dependency `yt-dlp`.
2. Menjalankan analyze URL.
3. Menjalankan download.
4. Membaca output log dari proses `yt-dlp`.

`src/format_utils.py`

Berisi fungsi untuk:

1. Klasifikasi format.
2. Membaca ukuran file.
3. Mengubah ukuran byte menjadi B, KB, MB, GB.
4. Menghitung estimasi ukuran gabungan video + audio.
5. Validasi format sesuai mode download.

`src/ffprobe_utils.py`

Berisi fungsi untuk:

1. Mengecek dependency `ffmpeg` dan `ffprobe`.
2. Menjalankan `ffprobe` pada file hasil download.
3. Membaca apakah file punya video, audio, resolusi, codec video, dan codec audio.

`requirements.txt`

Minimal berisi:

`PySide6`

`README.md`

Berisi panduan install, menjalankan aplikasi, dependency yang dibutuhkan, dan penjelasan mode download.

## 8. Dependency Eksternal

Aplikasi membutuhkan:

1. `yt-dlp`
2. `ffmpeg`
3. `ffprobe`

Saat aplikasi dibuka, lakukan pengecekan:

1. `yt-dlp --version`
2. `ffmpeg -version`
3. `ffprobe -version`

Jika `yt-dlp` tidak ditemukan, tampilkan error karena aplikasi tidak bisa berjalan normal.

Jika `ffmpeg` tidak ditemukan, tampilkan warning karena merge video + audio dan convert audio bisa gagal.

Jika `ffprobe` tidak ditemukan, tampilkan warning karena verifikasi hasil akhir tidak tersedia.

## 9. Workflow Utama

Alur utama aplikasi:

1. User membuka aplikasi.
2. User memasukkan URL video.
3. User menekan tombol Analyze.
4. Aplikasi menjalankan `yt-dlp -J --no-playlist "URL"`.
5. Aplikasi membaca output JSON.
6. Aplikasi menampilkan metadata video.
7. Aplikasi menampilkan daftar format asli.
8. Aplikasi mengklasifikasikan format menjadi video only, audio only, dan combined.
9. User memilih mode download.
10. User memilih format yang sesuai.
11. Aplikasi menampilkan estimasi ukuran.
12. User menekan tombol Download.
13. Aplikasi menjalankan command `yt-dlp`.
14. Log download tampil realtime.
15. Setelah selesai, aplikasi menampilkan path file hasil.
16. Jika `ffprobe` tersedia, aplikasi memverifikasi hasil file.

## 10. Analyze URL

Saat tombol Analyze ditekan, backend lokal aplikasi menjalankan:

`yt-dlp -J --no-playlist "URL"`

Aturan penting:

1. Jangan parsing output dari `yt-dlp -F`.
2. Jangan mengandalkan teks tabel dari terminal.
3. Gunakan JSON dari `yt-dlp -J`.
4. Semua format harus berasal dari field `formats` pada JSON.
5. Semua metadata harus berasal dari JSON.

Jika analyze gagal, tampilkan pesan error yang jelas di UI dan log.

## 11. Metadata Video yang Ditampilkan

Setelah analyze berhasil, tampilkan:

1. Title.
2. Uploader atau channel.
3. Duration.
4. Webpage URL.
5. Thumbnail URL atau preview thumbnail jika mudah diterapkan.
6. Jumlah format yang ditemukan.

Jika data tidak tersedia, tampilkan `Unknown`.

## 12. Klasifikasi Format

Format diambil dari field `formats` dalam JSON `yt-dlp`.

Klasifikasi harus berdasarkan `vcodec` dan `acodec`.

### 12.1 Video Only

Format dikategorikan sebagai video only jika:

`vcodec != "none"` dan `acodec == "none"`

Artinya:

1. Format punya video.
2. Format tidak punya audio.
3. Format ini valid untuk mode Video Only.
4. Format ini juga bisa dipasangkan dengan audio only untuk mode Video + Audio.

### 12.2 Audio Only

Format dikategorikan sebagai audio only jika:

`vcodec == "none"` dan `acodec != "none"`

Artinya:

1. Format tidak punya video.
2. Format punya audio.
3. Format ini valid untuk mode Audio Only.
4. Format ini bisa dipasangkan dengan video only untuk mode Video + Audio.

### 12.3 Combined

Format dikategorikan sebagai combined jika:

`vcodec != "none"` dan `acodec != "none"`

Artinya:

1. Format punya video.
2. Format punya audio.
3. Format ini bisa langsung digunakan untuk mode Video + Audio.

### 12.4 Unknown

Jika format tidak memenuhi tiga kategori di atas, tampilkan sebagai unknown atau abaikan dari pilihan download utama.

Unknown format boleh tampil di tabel, tetapi tidak boleh dipilih untuk download kecuali validasinya jelas.

## 13. Tabel Format

Tabel format harus menampilkan data asli dari JSON `yt-dlp`.

Kolom minimal:

1. `format_id`
2. `type`
3. `ext`
4. `resolution`
5. `width`
6. `height`
7. `fps`
8. `vcodec`
9. `acodec`
10. `filesize`
11. `filesize_approx`
12. `size_label`
13. `tbr`
14. `vbr`
15. `abr`
16. `format_note`

Jika nilai tidak tersedia, tampilkan `-` atau `Unknown`.

## 14. Aturan Ukuran File

Aplikasi tidak boleh mengarang ukuran file.

Urutan membaca ukuran:

1. Jika `filesize` tersedia, gunakan sebagai ukuran pasti.
2. Jika `filesize` tidak tersedia tetapi `filesize_approx` tersedia, gunakan sebagai estimasi.
3. Jika keduanya tidak tersedia, tampilkan `Unknown`.

Format ukuran harus human readable:

1. B
2. KB
3. MB
4. GB

Contoh tampilan:

1. `18.5 MB`
2. `~24.8 MB`
3. `1.2 GB`
4. `Unknown`

Tanda `~` digunakan jika ukuran berasal dari `filesize_approx`.

## 15. Estimasi Ukuran Berdasarkan Mode

### 15.1 Video Only

Estimasi ukuran = ukuran format video only yang dipilih.

Jika tidak tersedia, tampilkan `Unknown`.

### 15.2 Audio Only

Estimasi ukuran = ukuran format audio only yang dipilih.

Jika convert to MP3 aktif, tampilkan catatan bahwa ukuran akhir MP3 bisa berbeda dari estimasi sumber.

### 15.3 Video + Audio dengan Combined Format

Estimasi ukuran = ukuran format combined yang dipilih.

Jika tidak tersedia, tampilkan `Unknown`.

### 15.4 Video + Audio dengan Video Only + Audio Only

Estimasi ukuran = ukuran video only + ukuran audio only.

Jika salah satu ukuran tidak tersedia, tampilkan `Unknown / partial estimate`.

## 16. Mode Download

Aplikasi memiliki tiga mode utama:

1. Video + Audio
2. Video Only
3. Audio Only

## 17. Mode Video + Audio

Mode Video + Audio punya dua cara:

1. Menggunakan satu format combined.
2. Menggunakan satu format video only + satu format audio only.

Jika user memilih combined format, command:

`yt-dlp --no-playlist -f "<combined_id>" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"`

Jika user memilih video only + audio only, command:

`yt-dlp --no-playlist -f "<video_id>+<audio_id>" --merge-output-format "mp4/mkv" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"`

Validasi wajib:

1. Jika memilih combined, format harus punya video dan audio.
2. Jika memilih video + audio terpisah, format video harus video only.
3. Jika memilih video + audio terpisah, format audio harus audio only.
4. Jangan izinkan audio only dipilih sebagai video.
5. Jangan izinkan video only dipilih sebagai audio.

Catatan:

Jangan paksa semua hasil menjadi MP4. Gunakan `--merge-output-format "mp4/mkv"` agar container bisa menyesuaikan codec.

## 18. Mode Video Only

Mode Video Only hanya boleh memakai format video only.

Command:

`yt-dlp --no-playlist -f "<video_id>" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s VIDEO_ONLY [%(id)s].%(ext)s" "URL"`

Validasi wajib:

`vcodec != "none"` dan `acodec == "none"`

Larangan penting:

1. Jangan pakai selector `bv*`.
2. Jangan izinkan format combined.
3. Jangan izinkan format audio only.
4. Jangan memilih berdasarkan dropdown resolusi statis.
5. Pilihan harus berasal dari format asli JSON `yt-dlp`.

Kriteria berhasil:

File hasil download benar-benar punya video dan tidak punya audio.

## 19. Mode Audio Only

Mode Audio Only hanya boleh memakai format audio only.

Command tanpa convert:

`yt-dlp --no-playlist -f "<audio_id>" -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s AUDIO_ONLY [%(id)s].%(ext)s" "URL"`

Tambahkan checkbox `Convert to MP3`.

Jika Convert to MP3 aktif, command:

`yt-dlp --no-playlist -f "<audio_id>" -x --audio-format mp3 --audio-quality 0 -o "C:\Users\mlfad\downloads\ytdlp\%(title).120s [%(id)s].%(ext)s" "URL"`

Validasi wajib:

`vcodec == "none"` dan `acodec != "none"`

Kriteria berhasil:

File hasil download benar-benar punya audio dan tidak punya video.

## 20. Resolusi dan Filter Format

Aplikasi boleh menyediakan filter untuk memudahkan melihat format.

Contoh filter:

1. All
2. Video Only
3. Audio Only
4. Combined
5. 144p
6. 240p
7. 360p
8. 480p
9. 720p
10. 1080p
11. 1440p
12. 2160p

Namun filter resolusi hanya boleh menyaring format yang memang tersedia dari JSON.

Jangan membuat pilihan resolusi palsu.

Contoh:

Jika video tidak punya format 240p, maka aplikasi tidak boleh memaksa pilihan 240p sebagai download.

## 21. Desain UI

Aplikasi memakai dark theme sederhana.

Layout utama:

1. Header aplikasi.
2. Catatan kecil: `Gunakan hanya untuk konten yang memang Anda punya hak atau izin untuk unduh.`
3. Status dependency:

   * yt-dlp
   * ffmpeg
   * ffprobe
4. Input URL.
5. Tombol Analyze.
6. Metadata video.
7. Pilihan mode download.
8. Pilihan format.
9. Tabel format.
10. Estimasi ukuran.
11. Tombol Download.
12. Tombol Open Downloads Folder.
13. Tombol Clear Log.
14. Area log.
15. Status akhir.
16. Hasil verifikasi ffprobe jika tersedia.

UI tidak perlu terlalu mewah. Yang penting jelas, stabil, dan akurat.

## 22. Progress dan Log

Saat analyze atau download berjalan:

1. UI tidak boleh freeze.
2. Gunakan QThread atau worker thread.
3. Log stdout/stderr dari `yt-dlp` harus tampil realtime.
4. Status proses harus berubah sesuai keadaan.

Status minimal:

1. Idle
2. Analyzing
3. Ready
4. Downloading
5. Finished
6. Failed

Log harus menampilkan proses dengan jelas agar mudah debug jika gagal.

## 23. Path File Hasil

Setelah download selesai, aplikasi harus menampilkan path file hasil.

Gunakan cara paling aman:

1. Tambahkan opsi `--print after_move:filepath` jika bisa.
2. Jika tidak berhasil, parse output `yt-dlp`.
3. Jika masih tidak berhasil, cari file terbaru di folder download setelah proses selesai.

Path hasil harus mengarah ke:

`C:\Users\mlfad\downloads\ytdlp`

## 24. Verifikasi Hasil dengan ffprobe

Jika `ffprobe` tersedia, setelah download selesai aplikasi menjalankan:

`ffprobe -v error -show_streams -of json "FILE_PATH"`

Dari hasil ffprobe, tampilkan:

1. has_video: true/false
2. has_audio: true/false
3. video codec
4. audio codec
5. width
6. height
7. duration jika tersedia

Validasi hasil:

Mode Video Only harus menghasilkan:

`has_video = true`

`has_audio = false`

Mode Audio Only harus menghasilkan:

`has_video = false`

`has_audio = true`

Mode Video + Audio harus menghasilkan:

`has_video = true`

`has_audio = true`

Jika hasil tidak sesuai, tampilkan warning di UI.

## 25. Error Handling

Aplikasi harus menangani error berikut:

1. URL kosong.
2. URL tidak valid.
3. `yt-dlp` tidak ditemukan.
4. `ffmpeg` tidak ditemukan.
5. `ffprobe` tidak ditemukan.
6. Analyze gagal.
7. JSON gagal diparse.
8. Tidak ada format tersedia.
9. Format yang dipilih tidak sesuai mode.
10. Download gagal.
11. File hasil tidak ditemukan.
12. Verifikasi ffprobe gagal.
13. Folder output tidak bisa dibuat.
14. Permission error pada folder download.

Pesan error harus jelas dan mudah dipahami.

## 26. README yang Harus Dibuat

README harus menjelaskan:

1. Nama project.
2. Deskripsi singkat.
3. Bahwa aplikasi ini desktop GUI lokal.
4. Bahwa aplikasi ini bukan web.
5. Dependency yang dibutuhkan:

   * Python 3
   * yt-dlp
   * ffmpeg
   * ffprobe
6. Cara install dependency Python.
7. Cara menjalankan aplikasi.
8. Lokasi folder hasil download.
9. Penjelasan mode:

   * Video + Audio
   * Video Only
   * Audio Only
10. Catatan penggunaan legal dan etis.

## 27. requirements.txt

Minimal:

`PySide6`

Boleh menambahkan dependency kecil jika benar-benar diperlukan, tetapi hindari dependency berat.

## 28. Acceptance Criteria

Project dianggap berhasil jika:

1. Aplikasi bisa dijalankan dengan `python main.py`.
2. Aplikasi terbuka sebagai window desktop, bukan browser.
3. Aplikasi tidak membuat web server.
4. Analyze URL memakai `yt-dlp -J --no-playlist`.
5. Format yang tampil berasal dari JSON `yt-dlp`.
6. Video only, audio only, dan combined diklasifikasikan dengan benar.
7. Mode Video Only menghasilkan file tanpa audio.
8. Mode Audio Only menghasilkan file tanpa video.
9. Mode Video + Audio menghasilkan file dengan video dan audio.
10. Resolusi yang ditampilkan berasal dari format asli yang tersedia.
11. Estimasi ukuran tidak dikarang.
12. Jika ukuran tidak tersedia, aplikasi menampilkan Unknown.
13. Log download tampil realtime.
14. UI tidak freeze saat analyze/download.
15. File hasil tersimpan di `C:\Users\mlfad\downloads\ytdlp`.
16. Hasil akhir diverifikasi dengan ffprobe jika tersedia.
17. Tidak ada fitur browser, web app, login, cookies otomatis, atau bypass DRM.

## 29. Milestone Pengerjaan

### Milestone 1 - Setup Project

1. Buat struktur file.
2. Buat `main.py`.
3. Buat folder `src`.
4. Buat `requirements.txt`.
5. Buat window PySide6 dasar.
6. Buat folder output otomatis di `C:\Users\mlfad\downloads\ytdlp`.

### Milestone 2 - Dependency Check

1. Cek `yt-dlp`.
2. Cek `ffmpeg`.
3. Cek `ffprobe`.
4. Tampilkan status dependency di UI.

### Milestone 3 - Analyze URL

1. Jalankan `yt-dlp -J --no-playlist`.
2. Parse JSON.
3. Tampilkan metadata video.
4. Ambil daftar format.

### Milestone 4 - Format Classification

1. Implement video only.
2. Implement audio only.
3. Implement combined.
4. Implement human readable size.
5. Implement estimasi ukuran.

### Milestone 5 - Format Table dan Filter

1. Tampilkan format di tabel.
2. Tambahkan filter All, Video Only, Audio Only, Combined.
3. Tambahkan filter resolusi berdasarkan format yang tersedia.

### Milestone 6 - Download Mode

1. Implement Video + Audio combined.
2. Implement Video + Audio separate video/audio.
3. Implement Video Only.
4. Implement Audio Only.
5. Implement Convert to MP3.
6. Tambahkan validasi sebelum download.

### Milestone 7 - Log dan Progress

1. Jalankan analyze dan download di thread.
2. Tampilkan log realtime.
3. Pastikan UI tidak freeze.
4. Tampilkan status proses.

### Milestone 8 - Verifikasi Output

1. Ambil path file hasil.
2. Jalankan ffprobe.
3. Tampilkan hasil verifikasi.
4. Beri warning jika hasil tidak sesuai mode.

### Milestone 9 - Finishing

1. Rapikan UI dark theme.
2. Tambahkan README.
3. Test beberapa URL.
4. Pastikan tidak ada fitur web/browser.
5. Pastikan folder download default benar.

## 30. Catatan Teknis Penting

Selector `bv*` tidak boleh dipakai untuk Video Only.

Alasannya: `bv*` berarti format terbaik yang mengandung video, tetapi bisa saja format tersebut juga mengandung audio.

Untuk akurasi maksimal, jangan mengandalkan selector umum. Gunakan `format_id` dari JSON `yt-dlp`, lalu validasi berdasarkan `vcodec` dan `acodec`.

Validasi video only:

`vcodec != "none"` dan `acodec == "none"`

Validasi audio only:

`vcodec == "none"` dan `acodec != "none"`

Validasi combined:

`vcodec != "none"` dan `acodec != "none"`

Prinsip utama project ini:

Aplikasi harus sederhana, lokal, dan akurat. Lebih baik tampilan biasa saja tetapi hasil download benar, daripada UI terlihat bagus tetapi salah memilih format.
