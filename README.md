# Budapest Café Sales vs Weather (2023)

## Objective
This project analyzes how **daily weather conditions** (average temperature and precipitation)
affect **café sales behavior** in Budapest during 2023.

Focus:
- Hot beverages vs cold days
- Cold beverages vs warm days
- Cold beverages vs warm days
- Monthly sales-weather trends

## Tech Stack
- AWS S3 (data lake)
- AWS Glue (crawlers + catalog)
- AWS Lambda (weather ingestion from Open-Meteo)
- Amazon Athena (SQL analytics)

## Data
- Sales: synthetic daily café sales dataset (2023)
- Weather: Open-Meteo historical daily weather for Budapest (2023)

## Output
- Clean joined dataset (sales + weather)
- SQL queries proving temperature effect on hot vs cold beverage demand
