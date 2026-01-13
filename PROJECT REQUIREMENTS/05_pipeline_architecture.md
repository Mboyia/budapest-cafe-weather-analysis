# System Architecture
## Overview

The project implements a serverless AWS-based data pipeline that integrates
internal sales data with external weather data to analyze demand behavior.


### Components
1. **AWS Lambda**
   - Pulls historical weather data from the Open-Meteo API
   - Stores raw weather data in Amazon S3

2. **Amazon S3**
   - Raw zone: weather CSV and synthetic sales data
   - Curated zone: cleaned and joined datasets

3. **AWS Glue**
   -Cleans weather and sales data.
   - Deduplicates weather records to one row per day.
   - Joins sales and weather data on date.
   - Writes curated Parquet output.

4. **Amazon Athena**
   - Queries cleaned and curated datasets
   - Performs analytical SQL queries

## Architecture Flow

Sales CSV (S3)  
↓  
Weather CSV (S3 via Lambda)  
↓  
AWS Glue ETL (clean + join)  
↓  
Curated Table (`sales_weather_2023`)  
↓  
Athena Analysis Queries

## Design Principles
- Serverless and scalable
- Separation of raw and curated data
- SQL-based analytics for transparency and reproducibility

## Cost Considerations

This architecture is cost-efficient and suitable for small to medium datasets:

- **AWS Lambda**: Pay-per-execution, minimal cost due to low runtime.
- **Amazon S3**: Low-cost object storage for raw and curated data.
- **AWS Glue**: On-demand ETL jobs, suitable for batch processing.
- **Amazon Athena**: Pay-per-query, optimized through Parquet storage.

The serverless design minimizes operational overhead while supporting scalability.
