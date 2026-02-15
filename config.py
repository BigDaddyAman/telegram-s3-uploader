import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

ALLOWED_USERS = os.getenv("ALLOWED_USERS", "")
if ALLOWED_USERS:
    ALLOWED_USERS = {int(x.strip()) for x in ALLOWED_USERS.split(",")}
else:
    ALLOWED_USERS = set()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_REGION = os.getenv("S3_REGION")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")

DOWNLOAD_DIR = "downloads"

ENABLE_PRESIGNED_URL = os.getenv(
    "ENABLE_PRESIGNED_URL", "true"
).lower() == "true"

PRESIGNED_EXPIRE_SECONDS = int(
    os.getenv("PRESIGNED_EXPIRE_SECONDS", "3600")
)

S3_MAX_CONCURRENCY = int(os.getenv("S3_MAX_CONCURRENCY", "6"))
S3_MULTIPART_THRESHOLD_MB = int(os.getenv("S3_MULTIPART_THRESHOLD_MB", "100"))
S3_MULTIPART_CHUNK_MB = int(os.getenv("S3_MULTIPART_CHUNK_MB", "50"))

MAX_PARALLEL_UPLOADS = int(os.getenv("MAX_PARALLEL_UPLOADS", "3"))

required = [
    "API_ID",
    "API_HASH",
    "BOT_TOKEN",
    "S3_ACCESS_KEY",
    "S3_SECRET_KEY",
    "S3_BUCKET",
]

for var in required:
    if not globals().get(var):
        raise RuntimeError(f"Missing env var: {var}")
