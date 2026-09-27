"""
visualize.py
Reads Spark + MapReduce output CSVs and generates charts using Matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

SPARK_DIR = "../output/spark_results"
MR_DIR = "../output/mapreduce_results"
CHART_DIR = "."  # we're already inside charts/

plt.style.use("dark_background")  # matches your reference report's style

def save_chart(fig, filename):
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")

# ---------- 1. Average Rating by Genre ----------
df = pd.read_csv(f"{SPARK_DIR}/genre_avg_rating.csv")
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(df["genre"], df["avg_rating"], color="mediumseagreen")
ax.set_xlabel("Average Rating")
ax.set_title("Average Rating by Genre [PySpark Analysis]")
ax.invert_yaxis()  # highest at top
save_chart(fig, "1_genre_avg_rating.png")

# ---------- 2. Top 10 Highest-Rated Movies ----------
df = pd.read_csv(f"{SPARK_DIR}/top_10_movies.csv")
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(df["title"], df["avg_rating"], color="orchid")
ax.set_xlabel("Average Rating")
ax.set_title("Top 10 Highest-Rated Movies (min 50 ratings) [PySpark Analysis]")
ax.invert_yaxis()
save_chart(fig, "2_top_10_movies.png")

# ---------- 3. Most Active Users ----------
df = pd.read_csv(f"{SPARK_DIR}/top_10_active_users.csv")
labels = [f"User {row.user_id} ({row.city})" for row in df.itertuples()]
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(labels, df["total_ratings"], color="cornflowerblue")
ax.set_xlabel("Total Ratings Given")
ax.set_title("Top 10 Most Active Users [PySpark Analysis]")
ax.invert_yaxis()
save_chart(fig, "3_active_users.png")

# ---------- 4. Rating Distribution ----------
df = pd.read_csv(f"{SPARK_DIR}/rating_distribution.csv")
fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(df["rating"].astype(str), df["count"], color="tomato")
ax.set_xlabel("Rating Value")
ax.set_ylabel("Number of Ratings")
ax.set_title("Rating Distribution (50,000 ratings) [PySpark Analysis]")
save_chart(fig, "4_rating_distribution.png")

# ---------- 5. Ratings Trend Over Years ----------
df = pd.read_csv(f"{SPARK_DIR}/yearly_trend.csv")
fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.plot(df["year"], df["num_ratings"], color="crimson", marker="o", label="# Ratings")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Ratings", color="crimson")
ax2 = ax1.twinx()
ax2.plot(df["year"], df["avg_rating"], color="gold", marker="s", linestyle="--", label="Avg Rating")
ax2.set_ylabel("Average Rating", color="gold")
fig.suptitle("Ratings Trend Over Years [PySpark Analysis]")
save_chart(fig, "5_yearly_trend.png")

# ---------- 6. Genre Popularity (Donut Chart) ----------
df = pd.read_csv(f"{SPARK_DIR}/genre_popularity.csv")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df["count"], labels=df["genre"], autopct="%1.1f%%",
       wedgeprops=dict(width=0.4))
ax.set_title("Genre Popularity (% of Movies per Genre) [PySpark Analysis]")
save_chart(fig, "6_genre_popularity.png")

# ---------- 7. MapReduce: Top 20 Movies by Avg Rating ----------
df = pd.read_csv(f"{MR_DIR}/avg_rating_per_movie.csv", sep="\t")
df_top20 = df.sort_values("avg_rating", ascending=False).head(20)
fig, ax = plt.subplots(figsize=(9, 8))
ax.barh(df_top20["movie_id"].astype(str), df_top20["avg_rating"], color="mediumaquamarine")
ax.set_xlabel("Average Rating")
ax.set_title("Top 20 Movies - Average Rating [Hadoop MapReduce Analysis]")
ax.invert_yaxis()
save_chart(fig, "7_mapreduce_top20.png")

# ---------- 8. MapReduce: Rating Frequency ----------
df = pd.read_csv(f"{MR_DIR}/rating_frequency.csv", sep="\t", header=None, names=["rating", "count"])
df = df.sort_values("rating")
fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(df["rating"].astype(str), df["count"], color="slateblue")
ax.set_xlabel("Rating Value")
ax.set_ylabel("Frequency")
ax.set_title("Rating Frequency Distribution [Hadoop MapReduce Analysis]")
save_chart(fig, "8_mapreduce_rating_freq.png")

print("\nAll 8 charts generated successfully.")