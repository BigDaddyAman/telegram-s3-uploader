# Security Policy

## Supported versions

Only the latest version of this project is supported.

If you’re running an older version, please update before reporting issues.

---

## Reporting a security issue

If you discover a security issue, please **do not open a public issue**.

Instead:
- Open a GitHub Security Advisory  
  or
- Contact the maintainer privately (if contact info is available)

This helps prevent accidental exposure while the issue is being fixed.

---

## Security notes

- This bot uploads files to **private S3-compatible storage**
- Files are accessed using **temporary presigned URLs**
- Storage credentials are never shared with Telegram users
- Bot access can be restricted using an allowlist
- No public access is enabled by default

---

## Responsibility

You are responsible for:
- Protecting your credentials
- Controlling who can use your bot
- Running the bot in an environment you trust

This project is provided as-is and is intended for **private file upload and backup use cases**.
