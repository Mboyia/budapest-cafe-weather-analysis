# Implementation & Results

## Data Ingestion

- AWS Lambda retrieves historical weather data using the Open-Meteo API.
- Weather data is stored as CSV files in Amazon S3.
- Synthetic café sales data is uploaded to S3.

## Data Processing

- AWS Glue cleans and validates sales data.
- Weather data is deduplicated to ensure one record per day.
- Sales and weather datasets are joined on date.
- The curated dataset is written in Parquet format to S3.

## Data Analysis

- Amazon Athena is used to query the curated dataset.
- Temperature categories are defined as Cold (<10°C), Mild (10–20°C), and Hot (>20°C).
- Sales performance is analyzed across temperature and monthly trends.

## Results Interpretation

- Hot beverages dominate sales during cold weather.
- Cold beverages outperform during hot weather.
- Mild temperatures show balanced demand patterns.

The results confirm that weather is a strong external driver of beverage sales
and can be leveraged for operational and strategic decision-making.
