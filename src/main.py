import yaml
import os
import db
from google_play import GooglePlayDownloader


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "../config.yaml")) as config_file:
        return yaml.safe_load(config_file)


if __name__ == "__main__":
    # directory to temporary place all csv files.
    stats_dir = os.path.dirname(__file__), "..", "stats",
    config = read_config()
    google_play_config = config["google_play"]
    db_config = config["db"]

    # init the db session.
    db_sessions = db.connect_to_db(
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
