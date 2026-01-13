# Data Sources

## 1. Café Sales Data
- Type: Synthetic dataset
- Format: CSV
- Records: Daily sales by product category
- Key Fields:
  - date
  - city
  - store_id
  - product_category
  - units_sold
  - revenue_eur

## 2. Weather Data
- Source: Open-Meteo Historical Weather API
- Format: CSV (generated via Lambda)
- Location: Budapest (47.4979, 19.0402)
- Fields:
  - date
  - avg_temp (°C)
  - precipitation (mm)

## Data Validity
- Weather data spans all 365 days of 2023
- Sales data contains multiple rows per day (by store and category)
