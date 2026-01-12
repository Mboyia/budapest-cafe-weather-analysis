SELECT
    temp_category,
    product_category,
    SUM(units_sold) AS total_units_sold,
    ROUND(SUM(revenue_eur), 2) AS total_revenue_eur,
    ROUND(AVG(units_sold), 1) AS avg_units_per_row
FROM synthetic_curated_db.sales_weather_2023_labeled
WHERE product_category IN ('Hot Beverages', 'Cold Beverages')
GROUP BY
    temp_category,
    product_category
ORDER BY
    temp_category,
    product_category;
