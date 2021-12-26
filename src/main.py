from sqlalchemy.orm import session
import yaml
import os
import db
import csv
from google_play import GooglePlayDownloader
from model import Crash, Install, Rating
from log import logger
from builder import InstallBuilder, RatingBuilder, CrashBuilder


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "../config.yaml")) as config_file:
        return yaml.safe_load(config_file)


def start_export():
    # directory to temporary place all csv files.
    stats_dir = os.path.join(os.path.dirname(__file__), "..", "tmp")
    config = read_config()
    google_play_config = config["google_play"]
    db_config = config["db"]

    # init the db session.
    db_handler = db.DbHandler(
        db_config["user"],
        db_config["password"],
        db_config["host"],
        db_config["port"],
        db_config["database_name"]
    )

    downloader = GooglePlayDownloader(
        google_play_config["id"],
        stats_dir,
        google_play_config["path_to_service_account_json"],
        google_play_config["cloud_storage_bucket"]
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
