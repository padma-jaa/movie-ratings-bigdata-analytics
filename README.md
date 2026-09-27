# Movie Ratings Analytics System — Apache Spark (PySpark) + Hadoop MapReduce

A Big Data mini-project that generates a synthetic movie ratings dataset (500 movies, 1,000 users, 50,000 ratings) and analyses it two ways: **Apache Spark** (primary, distributed DataFrame processing) and **Hadoop MapReduce** (Python Streaming, classic Map–Shuffle–Reduce), then visualizes both sets of results with **Matplotlib**.

## Project Structure

```
movie_ratings_project/
│
├── data/
│   ├── generate_dataset.py     → creates movies.csv, users.csv, ratings.csv
│   ├── movies.csv
│   ├── users.csv
│   └── ratings.csv
│
├── spark_analysis/
│   └── movie_analysis_spark.py → 6 PySpark DataFrame analyses
│
├── mapreduce/
│   ├── mapper.py / reducer.py                    → Job 1: avg rating per movie
│   ├── mapper_rating_freq.py / reducer_rating_freq.py → Job 2: rating frequency
│   ├── mapper_genre_count.py / reducer_genre_count.py → Job 3: genre movie count
│   └── run_mapreduce.py         → runs all 3 jobs (mapper | sort | reducer, in Python)
│
├── output/
│   ├── spark_results/           → 6 CSVs from Spark
│   └── mapreduce_results/       → 3 CSVs from MapReduce
│
└── charts/
    └── visualize.py             → generates all PNG charts from the output CSVs
```

## How to Run It End-to-End

```cmd
cd data
python generate_dataset.py

cd ../spark_analysis
python movie_analysis_spark.py

cd ../mapreduce
python run_mapreduce.py

cd ../charts
python visualize.py
```

## What Each Stage Does (for your demo explanation)

### 1. Dataset Generation
A Python script uses `random` and `Faker` to programmatically create three CSV files — no downloaded dataset. Movies get 1–3 random genres (pipe-separated, e.g. `Comedy|Action`), users get demographic info across 10 Indian cities, and 50,000 ratings connect random user–movie pairs with a rating from 1.0–5.0 (half-point steps) and a random date between 2015–2024.

**Key talking point:** every rating/genre/city is chosen with *equal* random probability — this is why the analysis later shows a flat, uniform distribution rather than a realistic skew. Be ready to explain this if asked why nothing looks "biased" like a real streaming platform would be.

### 2. Spark Processing (PySpark)
Loads all 3 CSVs into Spark DataFrames (`local[*]` mode = uses all CPU cores) and runs 6 DataFrame-API analyses: genre-wise average rating, top 10 movies, most active users, rating distribution, yearly trend, and genre popularity. Each result is converted to pandas and saved as a clean single CSV (Spark's native writer creates messy multi-part folders, so we bypass that).

**Key talking point:** this demonstrates the DataFrame API's `groupBy`/`agg`/`join`/`explode` operations — the "HiveQL-equivalent" style of distributed querying.

### 3. Hadoop MapReduce (Python Streaming)
Three separate Map → Shuffle → Reduce jobs, each following the same pattern:
- **Mapper**: reads input line by line, emits `key\tvalue` pairs to stdout
- **Shuffle**: the emitted lines are sorted by key (this is literally what `sort` does in real Hadoop Streaming)
- **Reducer**: reads the *sorted* stream, and since same-key lines are now adjacent, aggregates by detecting "did the key change?" — no need to hold the whole dataset in memory

Job 1 computes avg rating per movie (500 movies), Job 2 counts frequency per rating value (9 values), Job 3 counts movies per genre (15 genres).

**Key talking point:** this is run locally via Python's `subprocess` module piping mapper output into the reducer, but it's functionally identical to the real Hadoop Streaming command:
```
cat ratings.csv | python mapper.py | sort | python reducer.py
```

### 4. Visualization (Matplotlib)
Reads every output CSV and produces bar charts, horizontal bar charts, a dual-axis line chart, and a donut pie chart — covering both the Spark and MapReduce results side by side, so the two tools' outputs can be visually cross-checked against each other.

## Key Results (What to Say in the Demo)

- All pipeline stages ran successfully end-to-end: 500 movies → 1,000 users → 50,000 ratings → 6 Spark CSVs → 3 MapReduce CSVs → charts.
- Genre-wise average ratings clustered tightly around **~3.0** for every genre — a direct, explainable consequence of generating ratings with uniform random probability (not a bug).
- Rating distribution (1.0–5.0) came out **nearly flat**, each value getting close to 50,000 ÷ 9 ≈ 5,556 ratings.
- Fantasy was the most-tagged genre (**8.6%** of all genre tags); Sci-Fi and Musical were least common (**5.5%** each).
- The most active user gave ~75 ratings; the top 10 active users were spread across 6 different Indian cities.
- **Spark and MapReduce independently produced consistent results** on the same dataset (e.g. both show the same near-uniform rating frequency) — this cross-validation is the strongest technical point to make if asked "why two tools?"

## Anticipated Demo Questions

| Question | Answer |
|---|---|
| Why use two big data tools? | To show both the modern DataFrame-based approach (Spark) and the foundational Map-Shuffle-Reduce paradigm (Hadoop), and cross-validate that both produce consistent results on the same data. |
| Why is the data so uniform/flat? | The synthetic generator assigns ratings, genres and dates with equal random probability by design — a deliberate simplification for a from-scratch synthetic dataset, unlike real-world data which is naturally skewed. |
| Why pandas `.to_csv()` instead of Spark's `.write.csv()`? | Spark's native writer creates a folder of partitioned part-files, not a single clean CSV, and needs `winutils.exe` configured correctly on Windows. Converting to pandas first avoids both issues and gives one clean file per result. |
| How does the Reducer know when a group ends? | The Shuffle step sorts all lines by key first, so identical keys become adjacent in the stream — the reducer just checks "is this key the same as the last one?" to detect a group boundary, without loading everything into memory. |
| What would you improve with more time? | Real HDFS storage + Hive queries, Spark Streaming for real-time ingestion, MLlib-based recommendations, and a weighted/skewed rating generator for more realistic data. |
