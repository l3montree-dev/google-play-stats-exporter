import json
from typing import Union
from google.cloud import storage
import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from google.cloud.storage.bucket import Bucket, Blob
from log import logger
from utils import Utils


class GooglePlayDownloader():

    @staticmethod
    def date_to_google_cloud_str(d: date):
        return d.strftime('%Y%m')

    @staticmethod
    def google_cloud_str_to_date(string: str) -> date:
        return datetime.strptime(string, "%Y%m").date()
    # the root directory to store stats. A separate session directory will be created
    # when issuing an operation.
    stats_dir: str

    # the path to the service_account json
    path_to_service_account_json: str

    cloud_storage_bucket: str

    bucket: Bucket

    app_id: str

    def __init__(
        self,
        app_id: str,
        stats_dir: str,
        path_to_service_account_json: str,
        cloud_storage_bucket: str
    ):
        self.app_id = app_id
        self.stats_dir = stats_dir
        self.path_to_service_account_json = path_to_service_account_json
        self.cloud_storage_bucket = cloud_storage_bucket
        self.bucket = self._get_bucket()

    def download_all_since_last_synced(self, last_synced_date: date) -> list[str]:
        """
        downloads all stats since the last time it was synced.
        returns the directory where the new csv files are stored.
        """

        if last_synced_date == None:
            logger.info("Never synced. Syncing all stats")
            return self.download_all_stats()

        today = date.today()
        current = last_synced_date

        session_dir = self._create_session_dir()

        downloaded_files: list[str] = []
        while current <= today:
            logger.info("downloading: {}".format(
                current.strftime("%Y-%m")))
            stats = self.download_stat_of_date(current, session_dir)
            if len(stats) > 0:
                downloaded_files += stats
            current += relativedelta(months=1)

        return downloaded_files

    def _get_bucket(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_to_service_account_json
        client = storage.Client()

        bucket = client.get_bucket(self.cloud_storage_bucket)
        return bucket

    def _create_session_dir(self) -> str:
        dirname = os.path.join(self.stats_dir, Utils.random_string(10))
        os.makedirs(dirname, exist_ok=True)
        return dirname

    def download_stat_of_date(self, date: date, download_to: str) -> list[str]:
        prefixes = ["crashes", "installs", "ratings"]
        # predict the name of the today stat
        date_str = GooglePlayDownloader.date_to_google_cloud_str(date)
        downloaded_files = []
        for prefix in prefixes:
            looking_for_stat = "stats/{prefix}/{prefix}_{app_id}_{date}_overview.csv".format(
                prefix=prefix, app_id=self.app_id, date=date_str)
            try:
                logger.info("looking for stat: {}".format(looking_for_stat))
                blob = self.bucket.get_blob(looking_for_stat)
                filename = os.path.join(download_to, blob.name)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                logger.info("downloading: {} to {}".format(
                    looking_for_stat, filename))
                blob.download_to_filename(filename)
                downloaded_files.append(filename)
            except (Exception) as e:
                logger.warn(e)
        return downloaded_files

    def _get_earliest_stat(self) -> Union[date, None]:
        blobs: list[Blob] = self.bucket.list_blobs()

        earliest_date: date
        for blob in blobs:
            if "overview" in blob.name:
                # extract the date out of the blob name.
                l = blob.name.split("_")
                current_date = GooglePlayDownloader.google_cloud_str_to_date(
                    l[2])
                if earliest_date == None or earliest_date > current_date:
                    earliest_date = current_date
        return earliest_date

    def download_all_stats(self) -> list[str]:
        blobs = self.bucket.list_blobs()
        session_dir = self._create_session_dir()
        downloaded_files = []

        for blob in blobs:
            # only download overview names
            if "overview" in blob.name:
                b = self.bucket.get_blob(blob.name)
                blobPath = os.path.dirname(blob.name)
                subpath = os.path.join(self.stats_dir, blobPath)
                os.makedirs(subpath, exist_ok=True)
                fullpath = os.path.join(session_dir, blob.name)
                b.download_to_filename(fullpath)
                downloaded_files.append(fullpath)
        return downloaded_files
