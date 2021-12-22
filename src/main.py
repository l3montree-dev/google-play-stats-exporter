import yaml
import os
import google_play


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "../config.yaml")) as config_file:
        return yaml.safe_load(config_file)


if __name__ == "__main__":
    # directory to temporary place all csv files.
    stats_dir = os.path.dirname(__file__), "..", "stats",
    config = read_config()
    google_play.download_all_stats(stats_dir, config["google_play"]
                                   ["path_to_service_account_json"], config["google_play"]["cloud_storage_bucket"])
