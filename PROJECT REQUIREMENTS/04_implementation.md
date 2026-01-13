# Implementation & Results

## Step 1: Weather Data Ingestion
- I created S3 bucket and uploaded sales data which was stored as a CSV file into one of the raw folder.
- AWS Lambda pulls historical daily weather data for 2023
- Data is saved as CSV to Amazon S3

## Step 2: Weather Data Cleaning
- AWS Glue job:
  - Parses date fields
  - Casts temperature and precipitation to numeric types
  - Removes null or invalid records

## Step 3: Sales Data Preparation
- Synthetic sales CSV stored in S3
- Schema validated via Athena

## Step 4: Data Joining
- AWS Glue joins sales data with weather data on `date`
- Left join ensures all sales records are preserved
- Resulting dataset stored as `sales_weather_2023`

## Step 5: Querying
- Athena used to:
  - Validate row counts
  - Confirm weather matching
  - Perform analytical aggregations

## step 6: Data Analysis

- Amazon Athena is used to query the curated dataset.
- Temperature categories are defined as Cold (<10°C), Mild (10–20°C), and Hot (>20°C).
- Sales performance is analyzed across temperature and monthly trends.

## Results Interpretation

- Hot beverages dominate sales during cold weather.
- Cold beverages outperform during hot weather.
- Mild temperatures show balanced demand patterns.

The results confirm that weather is a strong external driver of beverage sales
and can be leveraged for operational and strategic decision-making.
