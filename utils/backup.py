# This script uploads files to an Amazon S3 (Simple Storage Service) bucket.
# It utilizes the boto3 library, which is the Amazon Web Services (AWS) SDK for Python.

# Read more at upload_file function docstring

import json
import logging
import os
import pathlib
import sys
import threading
from typing import Optional

from django.conf import settings

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

# Constant variables
KB = 1024
MB = KB * KB
GB = MB * KB

# Configure logging
logging.basicConfig(level=logging.INFO)

# S3 client instance
s3_client = boto3.client(
    's3',
    endpoint_url=settings.AWS_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)


class ProgressPercentage:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._size = float(os.path.getsize(file_path))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """
        To simplify, assume this is hooked up to a single file_path

        :param bytes_amount: uploaded bytes
        """
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (self._file_path,
                                             self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


def upload_file(file_path: str, bucket: str, object_name: Optional[str] = None):
    """
    Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_path
    if object_name is None:
        object_name = file_path

    # Upload the file
    try:
        # Set the desired multipart threshold value (400 MB)
        config = TransferConfig(
            multipart_threshold=400 * MB, max_concurrency=5)
        s3_client.upload_file(
            file_path,
            bucket,
            object_name,
            ExtraArgs={'ACL': 'public-read'},
            Callback=ProgressPercentage(file_path),
            Config=config
        )
    except ClientError as e:
        logging.error(e)
        return False

    return True


# file
object_name = 'file.png'
file_rel_path: str = os.path.join('files', object_name)
file_abs_path: str = os.path.join(base_directory, file_rel_path)

upload_file(file_abs_path, 'sample_bucket', object_name)
