import boto3
from botocore.client import Config
from config import (
    S3_ENDPOINT,
    S3_REGION,
    S3_ACCESS_KEY,
    S3_SECRET_KEY,
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
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expires,
    )
