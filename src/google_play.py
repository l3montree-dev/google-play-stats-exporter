import json
from google.cloud import client, storage
import os


def download_all_stats(stats_dir, path_to_service_account_json, cloud_storage_bucket):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_service_account_json
    client = storage.Client()

    bucket = client.get_bucket(cloud_storage_bucket)

    blobs = bucket.list_blobs()
    for blob in blobs:
        if "overview" in blob.name:
            b = bucket.get_blob(blob.name)
            blobPath = os.path.dirname(blob.name)
            subpath = os.path.join(stats_dir, blobPath)
            os.makedirs(subpath, exist_ok=True)
            fullpath = os.path.join(stats_dir, blob.name)
            b.download_to_filename(fullpath)
