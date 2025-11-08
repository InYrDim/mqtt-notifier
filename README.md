# MQTT Notifier dengan Ngrok dan Telegram

Proyek ini bertujuan untuk menjalankan *broker* MQTT menggunakan [Eclipse Mosquitto](https://mosquitto.org/) dan mengeksposnya ke internet publik menggunakan [Ngrok](https://ngrok.com/). Sebuah layanan notifikasi akan secara otomatis mengirimkan detail koneksi (host dan port) dari *tunnel* Ngrok ke obrolan Telegram setiap kali alamat publik berubah.

## Fitur

  - **Broker MQTT**: Menjalankan Mosquitto sebagai *broker* MQTT dalam kontainer Docker.
  - **Akses Publik**: Menggunakan Ngrok untuk membuat *tunnel* TCP publik ke *broker* MQTT.
  - **Notifikasi Real-time**: Layanan notifikasi Python memantau perubahan pada *tunnel* Ngrok dan mengirimkan detail koneksi terbaru ke Telegram.
  - **Setup Mudah**: Seluruh layanan diatur menggunakan Docker Compose untuk kemudahan instalasi dan penggunaan.

## Arsitektur

Proyek ini terdiri dari tiga layanan utama yang diatur dalam `docker-compose.yml`:

1.  **`mosquitto`**: Layanan *broker* MQTT. Konfigurasi dan data disimpan dalam volume untuk persistensi.
2.  **`ngrok`**: Membuat *tunnel* TCP dari internet publik ke layanan `mosquitto` pada port `1883`.
3.  **`notifier`**: Skrip Python yang berjalan secara berkala untuk:
      - Memeriksa API lokal Ngrok untuk mendapatkan alamat publik (*host* dan *port*) saat ini.
      - Jika alamat berubah dari yang terakhir dicatat, ia akan mengirim pesan notifikasi ke obrolan Telegram.
      - Menyimpan *port* terakhir yang dikirim ke sebuah file untuk menghindari notifikasi duplikat.

## Prasyarat

Sebelum memulai, pastikan Anda telah menginstal:

  - [Docker](https://www.docker.com/get-started)
  - [Docker Compose](https://docs.docker.com/compose/install/)

Anda juga memerlukan:

  - **Akun Ngrok**: Daftar di [dashboard.ngrok.com](https://dashboard.ngrok.com) untuk mendapatkan **AuthToken**.
  - **Bot Telegram**:
      - Buat bot baru dengan berbicara kepada [@BotFather](https://t.me/BotFather) di Telegram untuk mendapatkan **Token Bot**.
      - Dapatkan **Chat ID** Anda. Anda bisa mendapatkannya dengan mengirim pesan ke bot `@userinfobot`.

## Instalasi

1.  **Kloning Repositori**

    ```bash
    git clone https://github.com/inyrdim/mqtt-notifier.git
    cd mqtt-notifier
    ```

2.  **Buat File `.env`**
    Buat file bernama `.env` di direktori utama proyek dan isi dengan kredensial yang Anda dapatkan dari prasyarat.

    ```env
    # Dapatkan dari https://dashboard.ngrok.com/get-started/your-authtoken
    NGROK_AUTHTOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxx

    # Token Bot dari @BotFather
    TELEGRAM_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxx

    # ID Obrolan tujuan notifikasi
    TELEGRAM_CHAT_ID=xxxxxxxxxx
    ```

## Penggunaan

Jalankan semua layanan menggunakan Docker Compose:

```bash
docker-compose up -d
```

Setelah layanan berjalan, skrip notifikasi akan secara otomatis memonitor *tunnel* Ngrok. Ketika *tunnel* aktif dan alamat publiknya terdeteksi untuk pertama kali (atau berubah), Anda akan menerima pesan di Telegram seperti ini:

> 🌐 MQTT Broker Online
>
> 🔌 Ngrok Tunnel
> Host: 0.tcp.ap.ngrok.io
> Port: 12345

Anda sekarang dapat menggunakan *host* dan *port* tersebut untuk terhubung ke *broker* MQTT Anda dari mana saja.

Untuk menghentikan semua layanan, jalankan:

```bash
docker-compose down
```

## Struktur Proyek

```
.
├── .gitignore
├── docker-compose.yml   # Mengatur semua layanan (mosquitto, ngrok, notifier)
├── mosquitto.conf       # File konfigurasi untuk broker Mosquitto (opsional)
├── notifier/
│   ├── Dockerfile         # Dockerfile untuk membangun image layanan notifikasi
│   └── notify_ngrok.py  # Skrip Python untuk mengirim notifikasi
└── README.md
```