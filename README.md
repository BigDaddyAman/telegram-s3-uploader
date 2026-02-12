# Telegram → S3 Uploader Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Telegram-blue)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Framework](https://img.shields.io/badge/framework-Pyrofork%20(async)-green)
![Deploy](https://img.shields.io/badge/deploy-Railway-purple)
![Docker](https://img.shields.io/badge/docker-supported-blue)

A simple, private Telegram bot that uploads files to **any S3-compatible storage**
(AWS S3, Cloudflare R2, MinIO, etc.) and returns a **temporary presigned download link**.

This project is designed to be:
- Simple
- Safe by default
- Easy to deploy
- Easy to extend

---

## ✨ Features

- Upload files from Telegram to S3-compatible storage
- Supports documents, videos, audio, and photos
- Private bucket (no public access required)
- Temporary **presigned download links**
- User allowlist (private bot)
- Works on local machine, VPS, Docker, and Railway
- Clean, minimal codebase

---

## 📦 Supported Storage

This bot works with any S3-compatible provider, including:

- AWS S3
- Cloudflare R2
- MinIO (local NAS)
- Wasabi
- DigitalOcean Spaces
- Backblaze B2 (S3 API)

---

## 🔐 Security Model

- Files are uploaded to a **private bucket**
- Access is granted via **temporary presigned URLs**
- Links expire automatically
- Storage credentials are never exposed to users
- Bot usage can be restricted with an allowlist
- Local files are stored temporarily and cleaned up automatically

This bot is intended for **private file upload and backup use cases**.

---

## 🚀 Deployment

### ▶ Deploy on Railway

You can deploy this bot directly to Railway:

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/telegram-s3-uploader?referralCode=nIQTyp&utm_medium=integration&utm_source=template&utm_campaign=generic)

After deployment, set the required environment variables in the Railway dashboard.

> When deployed on Railway, this template attaches a Railway Bucket by default.
> You can remove it and configure any other S3-compatible storage via environment variables.

---

### ▶ Run locally

> Python 3.13 is supported. Python 3.11+ is recommended for widest compatibility.

#### 1. Clone the repository
```bash
git clone https://github.com/BigDaddyAman/telegram-s3-uploader
cd telegram-s3-uploader
```

#### 2. Create virtual environment
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure environment

Copy .env.example to .env and fill in your values:

```bash
cp .env.example .env
```

#### 5. Run the bot
```bash
python bot.py
```

---

### ▶ Run with Docker (build locally)

```bash
docker build -t telegram-s3-uploader .
docker run --env-file .env telegram-s3-uploader
```

---

## ⚙️ Environment Variables

| Variable | Description |
|----------|-------------|
| API_ID | Telegram API ID |
| API_HASH | Telegram API hash |
| BOT_TOKEN | Telegram bot token |
| ALLOWED_USERS | Allowed Telegram user IDs (comma-separated) |
| S3_ENDPOINT | Custom S3 endpoint (leave empty for AWS) |
| S3_REGION | S3 region (required for AWS) |
| S3_ACCESS_KEY | S3 access key |
| S3_SECRET_KEY | S3 secret key |
| S3_BUCKET | Bucket name |
| PRESIGNED_EXPIRE_SECONDS | Presigned link expiration time (seconds) |
| ENABLE_PRESIGNED_URL | Enable or disable presigned download links (`true` / `false`) |

---

## 📁 File Storage Layout

Uploaded files are stored using a simple structure:

> Files are downloaded to a temporary local directory and removed automatically after upload.

```
users/
└── <telegram_user_id>/
    └── YYYYMMDD_HHMMSS_filename.ext
```

This makes the storage easy to browse and suitable for backups.

---

## 🧭 Project Scope

This project is intentionally kept small and focused.

It is meant for:

- Personal backups
- Private file storage
- Archiving Telegram content you own or manage

Features related to public distribution, streaming, or content sharing are out of scope.

---

## 🤝 Contributing

Contributions are welcome!

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and project scope.

---

## 🔐 Security

If you discover a security issue, please follow the instructions in [SECURITY.md](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for details.