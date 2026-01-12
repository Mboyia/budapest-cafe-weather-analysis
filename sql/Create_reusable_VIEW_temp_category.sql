-- Join sales (string date) with weather (date) safely

CREATE OR REPLACE VIEW synthetic_sales_db.budapest_sales_weather_2023 AS
SELECT
  CAST(s.date AS date) AS date,
  s.city,
  s.store_id,
  s.product_category,
  CAST(s.units_sold AS integer) AS units_sold,
  CAST(s.revenue_eur AS double) AS revenue_eur,
  w.avg_temp,
  w.precipitation
FROM synthetic_sales_db.budapest_cafe_sales_2023_synthetic_csv s
LEFT JOIN synthetic_weather_db.budapest_weather_daily_clean w
  ON CAST(s.date AS date) = w.date;