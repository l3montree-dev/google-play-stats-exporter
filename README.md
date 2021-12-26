<img src="./logo.png">

# Google Play Console Statistics Exporter

The Stats-Exporter is a python script which downloads statistics from the `Google Play Console` and synchronizes them with a MySQL Database.

## Features

Synchronization of:

- `ratings` statistics
- `installs` statistics
- `crash` statistics

The statistics are downloaded from the Google play console using the Google cloud storage bucket. Google does already provide CSV files with statistics for each day (with a delay of about 3 days). This script builds database tables out of the downloaded CSV files and inserts all rows.

Before starting the sync, the script checks what months need to be downloaded. This makes it optimized to be used inside a daily cron job.

## Usage

A `.env` file needs to be provided or the following environment variables need to be set.

It should match the following scheme:

```yaml
GOOGLE_PLAY_APP_ID=de.app
PATH_TO_SERVICE_ACCOUNT_JSON=/path/to/service_account.json
CLOUD_STORAGE_BUCKET_URL=pubsite_prod_xxx

DB_USER=exporter
DB_PASSWORD=secret
DB_DATABASENAME=exporter
DB_HOST=127.0.0.1
DB_PORT=3306
```

Obtaining the necessary information:

1. `GOOGLE_PLAY_APP_ID`: The Application ID in the App Store. Can be extracted from the Google play URL. For example, the URL: `https://play.google.com/store/apps/details?id=de.stamplab` yields the ID as the `id` query parameter.
2. `service_account.json`: Checkout this documentation: https://support.google.com/googleplay/android-developer/answer/6135870?visit_id=637761055020524646-2114696062&p=stats_export&rd=1#export. **MAKE SURE** you provide at least the `Viewer` role to the service account. Otherwise, it won't appear in the list of service accounts in the Google play console (API-Access).
3. `CLOUD_STORAGE_BUCKET_URL`: All Apps > Download Stats > Ratings > Copy cloud storage URI button

The .env file needs to be stored in the root folder of the project.

Install the dependencies using:

```sh
pip install -r requirements.txt
```

Afterwards, call the script with:

```sh
python ./src/main.py
```
