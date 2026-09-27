"""
movie_analysis_spark.py
Loads movie ratings data into PySpark and runs analytical queries.
Saves each result as a clean CSV using pandas (avoids Spark's messy
multi-part output files, and avoids winutils.exe issues on Windows).
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

# ---------- SETUP ----------
spark = SparkSession.builder \
    .appName("MovieRatingsAnalysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")  # hide noisy warnings

DATA_DIR = "../data"
OUTPUT_DIR = "../output/spark_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- LOAD DATA ----------
movies = spark.read.csv(f"{DATA_DIR}/movies.csv", header=True, inferSchema=True)
users = spark.read.csv(f"{DATA_DIR}/users.csv", header=True, inferSchema=True)
ratings = spark.read.csv(f"{DATA_DIR}/ratings.csv", header=True, inferSchema=True)

print("Movies schema:")
movies.printSchema()
print("Ratings schema:")
ratings.printSchema()

def save(df, filename):
    """Convert Spark DataFrame -> pandas -> single clean CSV file."""
    path = f"{OUTPUT_DIR}/{filename}"
    df.toPandas().to_csv(path, index=False)
    print(f"Saved: {path}")

# ---------- 1. GENRE-WISE AVERAGE RATING ----------
genre_ratings = movies \
    .withColumn("genre", F.explode(F.split("genres", "\\|"))) \
    .join(ratings, "movie_id") \
    .groupBy("genre") \
    .agg(F.count("rating").alias("num_ratings"),
         F.avg("rating").alias("avg_rating")) \
    .orderBy(F.desc("avg_rating"))

save(genre_ratings, "genre_avg_rating.csv")

# ---------- 2. TOP 10 HIGHEST-RATED MOVIES (min 50 ratings) ----------
top_movies = ratings \
    .groupBy("movie_id") \
    .agg(F.count("rating").alias("num_ratings"),
         F.avg("rating").alias("avg_rating")) \
    .filter(F.col("num_ratings") >= 50) \
    .join(movies, "movie_id") \
    .orderBy(F.desc("avg_rating")) \
    .select("movie_id", "title", "genres", "num_ratings", "avg_rating") \
    .limit(10)

save(top_movies, "top_10_movies.csv")

# ---------- 3. MOST ACTIVE USERS (Top 10) ----------
active_users = ratings \
    .groupBy("user_id") \
    .agg(F.count("rating").alias("total_ratings"),
         F.avg("rating").alias("avg_rating")) \
    .join(users, "user_id") \
    .orderBy(F.desc("total_ratings")) \
    .select("user_id", "city", "occupation", "total_ratings", "avg_rating") \
    .limit(10)

save(active_users, "top_10_active_users.csv")

# ---------- 4. RATING DISTRIBUTION ----------
rating_dist = ratings \
    .groupBy("rating") \
    .count() \
    .orderBy("rating")

save(rating_dist, "rating_distribution.csv")

# ---------- 5. YEARLY RATING TREND ----------
year_trend = ratings \
    .withColumn("year", F.year(F.to_date("timestamp"))) \
    .groupBy("year") \
    .agg(F.count("rating").alias("num_ratings"),
         F.avg("rating").alias("avg_rating")) \
    .orderBy("year")

save(year_trend, "yearly_trend.csv")

# ---------- 6. GENRE POPULARITY (movie count per genre) ----------
genre_pop = movies \
    .withColumn("genre", F.explode(F.split("genres", "\\|"))) \
    .groupBy("genre") \
    .count() \
    .orderBy(F.desc("count"))

save(genre_pop, "genre_popularity.csv")

spark.stop()
print("\nSpark analysis complete. 6 CSV files saved.")