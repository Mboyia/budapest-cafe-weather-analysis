CREATE OR REPLACE VIEW synthetic_curated_db.sales_weather_monthly_trends AS
SELECT
    date_trunc('month', date) AS month,
    product_category,
    COUNT(*) AS rows,
    SUM(units_sold) AS total_units_sold,
    SUM(revenue_eur) AS total_revenue_eur,
    ROUND(AVG(avg_temp), 1) AS avg_monthly_temp
FROM synthetic_curated_db.sales_weather_2023
GROUP BY
    date_trunc('month', date),
    product_category
ORDER BY
    month,
    product_category;
