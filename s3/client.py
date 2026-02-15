import boto3
from botocore.client import Config
from boto3.s3.transfer import TransferConfig

from config import (
    S3_ENDPOINT,
    S3_REGION,
    S3_ACCESS_KEY,
    S3_SECRET_KEY,
    S3_MAX_CONCURRENCY,
    S3_MULTIPART_THRESHOLD_MB,
    S3_MULTIPART_CHUNK_MB,
)

S3_TRANSFER_CONFIG = TransferConfig(
    multipart_threshold=S3_MULTIPART_THRESHOLD_MB * 1024 * 1024,
    multipart_chunksize=S3_MULTIPART_CHUNK_MB * 1024 * 1024,
    max_concurrency=S3_MAX_CONCURRENCY,
    use_threads=True,
)

def get_s3_client():
    kwargs = {
        "aws_access_key_id": S3_ACCESS_KEY,
        "aws_secret_access_key": S3_SECRET_KEY,
        "config": Config(signature_version="s3v4"),
    }

    if S3_ENDPOINT:
        kwargs["endpoint_url"] = S3_ENDPOINT
        kwargs["region_name"] = S3_REGION or "us-east-1"
    else:
        if not S3_REGION:
            raise RuntimeError("AWS S3 requires S3_REGION")
        kwargs["region_name"] = S3_REGION

    return boto3.client("s3", **kwargs)


def generate_presigned_url(s3, bucket: str, key: str, expires: int):
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires,
    )
