import json
from google.cloud import client, storage
import os
from datetime import datetime


class GooglePlayDownloader():
    def __init__(
        self,
        # something like de.stamplab
        # the application id.
        app_id,
        stats_dir,
        path_to_service_account_json,
        cloud_storage_bucket
    ):
        self.stats_dir = stats_dir
        self.path_to_service_account_json = path_to_service_account_json
        self.cloud_storage_bucket = cloud_storage_bucket
        self.bucket = self._get_bucket()
        self.app_id = app_id

    def get_date_str():
        return datetime.today().strftime('%Y%m%d')

    def _get_bucket(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_to_service_account_json
        client = storage.Client()

        bucket = client.get_bucket(self.cloud_storage_bucket)
        return bucket

    def download_today_stats():
        prefixes = ["crashes", "installs", "ratings"]

        pass

    def download_all_stats(self):
        blobs = self.bucket.list_blobs()
        for blob in blobs:
            # only download overview names
            if "overview" in blob.name and self.app_id in blob.name:
                b = self.bucket.get_blob(blob.name)
                blobPath = os.path.dirname(blob.name)
                subpath = os.path.join(self.stats_dir, blobPath)
                os.makedirs(subpath, exist_ok=True)
                fullpath = os.path.join(self.stats_dir, blob.name)
                b.download_to_filename(fullpath)
