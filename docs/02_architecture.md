# System Architecture

## High-Level Architecture

The project follows a modern serverless data architecture using AWS managed services.

### Components
1. **AWS Lambda**
   - Pulls historical weather data from the Open-Meteo API
   - Stores raw weather data in Amazon S3

2. **Amazon S3**
   - Raw zone: weather CSV and synthetic sales data
   - Curated zone: cleaned and joined datasets

3. **AWS Glue**
   - Cleans raw weather data
   - Joins weather and sales datasets
   - Writes curated output tables

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
