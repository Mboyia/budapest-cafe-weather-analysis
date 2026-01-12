import boto3
import csv
import io
import json
import urllib.request
from datetime import datetime

s3 = boto3.client("s3")

BUCKET_NAME = "s3-synthetic"
BASE_PREFIX = "raw/weather/budapest/"
LAT = 47.4979
LON = 19.0402

WEATHER_API = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude={lat}&longitude={lon}"
    "&start_date={start}&end_date={end}"
    "&daily=temperature_2m_mean,precipitation_sum"
    "&timezone=Europe/Budapest"
)

def lambda_handler(event, context):
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    url = WEATHER_API.format(lat=LAT, lon=LON, start=start_date, end=end_date)

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    # Extract daily arrays
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temps = daily.get("temperature_2m_mean", [])
    precs = daily.get("precipitation_sum", [])

    if not (dates and temps and precs) or not (len(dates) == len(temps) == len(precs)):
        raise Exception("Daily arrays missing or lengths do not match")

    # Build CSV in-memory
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["date", "avg_temp", "precipitation"])

    for d, t, p in zip(dates, temps, precs):
        writer.writerow([d, t, p])

    s3_key = f"{BASE_PREFIX}budapest_weather_2023_daily.csv"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer.getvalue().encode("utf-8"),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "message": "CSV weather written to S3",
        "s3_path": f"s3://{BUCKET_NAME}/{s3_key}",
        "rows": len(dates)
    }
