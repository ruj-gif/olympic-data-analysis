from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType
import os

# ----------------------------
# Create Spark Session
# ----------------------------
spark = SparkSession.builder \
    .appName("Tokyo Olympics ETL") \
    .master("local[*]") \
    .getOrCreate()

# ----------------------------
# Paths
# ----------------------------
RAW_PATH = "data/raw/"
OUTPUT_PATH = "data/transformed/"

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ----------------------------
# Read CSV Files
# ----------------------------
athletes = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(RAW_PATH + "athletes.csv")

coaches = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(RAW_PATH + "coaches.csv")

entriesgender = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(RAW_PATH + "entriesgender.csv")

medals = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(RAW_PATH + "medals.csv")

teams = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(RAW_PATH + "teams.csv")

# ----------------------------
# Transformations
# ----------------------------

# Convert gender columns to integers
entriesgender = entriesgender \
    .withColumn("Female", col("Female").cast(IntegerType())) \
    .withColumn("Male", col("Male").cast(IntegerType())) \
    .withColumn("Total", col("Total").cast(IntegerType()))

# Convert medal columns to integers
medals = medals \
    .withColumn("Rank", col("Rank").cast(IntegerType())) \
    .withColumn("Gold", col("Gold").cast(IntegerType())) \
    .withColumn("Silver", col("Silver").cast(IntegerType())) \
    .withColumn("Bronze", col("Bronze").cast(IntegerType())) \
    .withColumn("Total", col("Total").cast(IntegerType())) \
    .withColumn("Rank by Total", col("Rank by Total").cast(IntegerType()))

# ----------------------------
# Write Transformed Data
# ----------------------------

athletes.repartition(1).write.mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH + "athletes")

coaches.repartition(1).write.mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH + "coaches")

entriesgender.repartition(1).write.mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH + "entriesgender")

medals.repartition(1).write.mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH + "medals")

teams.repartition(1).write.mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH + "teams")

print("\n==============================")
print("Transformation Completed!")
print("==============================")

spark.stop()