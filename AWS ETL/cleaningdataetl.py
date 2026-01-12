import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# -----------------------------
# CONFIG (EDIT THESE)
# -----------------------------
sales_db = "synthetic_sales_db"
sales_table = "budapest_cafe_sales_2023_synthetic_csv"

weather_db = "synthetic_weather_db"
weather_table = "budapest_weather_2023_daily_csv"

OUTPUT_PATH = "s3://s3-synthetic/curated/sales_weather_2023/"  # change if needed

# -----------------------------
# READ FROM GLUE CATALOG
# -----------------------------
sales_dyf = glueContext.create_dynamic_frame.from_catalog(
    database=sales_db,
    table_name=sales_table
)

weather_dyf = glueContext.create_dynamic_frame.from_catalog(
    database=weather_db,
    table_name=weather_table
)

sales_df = sales_dyf.toDF()
weather_df = weather_dyf.toDF()

# -----------------------------
# CLEAN SALES
# (remove corrupted rows like city=4.7 etc.)
# -----------------------------
# Ensure proper types + filter only valid Budapest rows
sales_clean = (
    sales_df
    .withColumn("date", F.to_date(F.col("date")))  # assumes 'YYYY-MM-DD'
    .withColumn("units_sold", F.col("units_sold").cast("int"))
    .withColumn("revenue_eur", F.col("revenue_eur").cast("double"))
    .filter(F.col("date").isNotNull())
    .filter(F.col("city") == "Budapest")
    .filter(F.col("store_id").startswith("BUD-"))
    .filter(F.col("product_category").isin("Hot Beverages", "Cold Beverages", "Pastries"))
    .filter(F.col("units_sold").isNotNull())
    .filter(F.col("revenue_eur").isNotNull())
)

# -----------------------------
# CLEAN + DEDUPE WEATHER
# (1 row per date)
# -----------------------------
weather_clean = (
    weather_df
    .withColumn("date", F.to_date(F.col("date")))  # assumes 'YYYY-MM-DD'
    .withColumn("avg_temp", F.col("avg_temp").cast("double"))
    .withColumn("precipitation", F.col("precipitation").cast("double"))
    .filter(F.col("date").isNotNull())
)

# Deduplicate by date (in case Glue read duplicates)
weather_daily = (
    weather_clean
    .groupBy("date")
    .agg(
        F.avg("avg_temp").alias("avg_temp"),
        F.avg("precipitation").alias("precipitation")
    )
)

# -----------------------------
# JOIN ON DATE
# -----------------------------
joined = (
    sales_clean
    .join(weather_daily, on="date", how="left")
)

# Optional: sanity columns for analysis
joined = joined.withColumn(
    "temp_group",
    F.when(F.col("avg_temp") < 10, F.lit("cold(<10C)"))
     .when((F.col("avg_temp") >= 10) & (F.col("avg_temp") <= 20), F.lit("mild(10-20C)"))
     .otherwise(F.lit("warm(>20C)"))
)

joined = joined.withColumn("month", F.month("date"))

# -----------------------------
# WRITE CURATED PARQUET
# -----------------------------
(
    joined
    .repartition(1)  # optional, makes fewer files for small datasets
    .write
    .mode("overwrite")
    .partitionBy("month")
    .parquet(OUTPUT_PATH)
)

job.commit()
