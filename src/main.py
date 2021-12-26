from sqlalchemy.orm import session
import yaml
import os
import db
import csv
from google_play import GooglePlayDownloader
from model import Crash, Install, Rating
from log import logger
from builder import InstallBuilder, RatingBuilder, CrashBuilder
from dotenv import load_dotenv


load_dotenv()


def start_export():
    # directory to temporary place all csv files.
    stats_dir = os.path.join(os.path.dirname(__file__), "..", "tmp")
    # init the db session.
    db_handler = db.DbHandler(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_DATABASENAME")
    )

    downloader = GooglePlayDownloader(
        os.getenv("GOOGLE_PLAY_APP_ID"),
        stats_dir,
        os.getenv("PATH_TO_SERVICE_ACCOUNT_JSON"),
        os.getenv("CLOUD_STORAGE_BUCKET_URL")
    )

    logger.info("start syncing")
    for builder in [InstallBuilder(), CrashBuilder(), RatingBuilder()]:
        logger.info("starting iteration for builder: {}".format(
            builder.get_prefix()))
        db_handler.sync_stats(
            downloader.download_all_since_last_synced(
                db_handler.get_last_date_synced(builder),
                builder,
            ),
            builder
        )


if __name__ == "__main__":
    start_export()
