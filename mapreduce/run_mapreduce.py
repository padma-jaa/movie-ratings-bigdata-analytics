"""
run_mapreduce.py
Replicates: cat ratings.csv | python mapper.py | sort | python reducer.py
Runs entirely in Python so it works identically on Windows/Mac/Linux.
"""

import subprocess
import os

DATA_FILE = "../data/ratings.csv"
OUTPUT_DIR = "../output/mapreduce_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Step 1: Run mapper.py, feeding it ratings.csv ----------
with open(DATA_FILE, "r", encoding="utf-8") as f:
    mapper_process = subprocess.run(
        ["python", "mapper.py"],
        stdin=f,
        capture_output=True,
        text=True
    )
mapped_output = mapper_process.stdout
print(f"Mapper produced {len(mapped_output.splitlines())} key-value pairs")

# ---------- Step 2: Sort (the "Shuffle" phase) ----------
lines = mapped_output.strip().split("\n")
# sort by movie_id (the key, before the tab) — numerically, not as text
sorted_lines = sorted(lines, key=lambda x: int(x.split("\t")[0]))
sorted_output = "\n".join(sorted_lines)
print("Shuffle (sort) phase complete")

# ---------- Step 3: Run reducer.py, feeding it sorted data ----------
reducer_process = subprocess.run(
    ["python", "reducer.py"],
    input=sorted_output,
    capture_output=True,
    text=True
)
reduced_output = reducer_process.stdout
print(f"Reducer produced {len(reduced_output.splitlines())} aggregated results")

# ---------- Save result ----------
output_path = f"{OUTPUT_DIR}/avg_rating_per_movie.csv"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("movie_id\tnum_ratings\tavg_rating\n")
    f.write(reduced_output)

print(f"Saved: {output_path}")

# ---------- JOB 2: Rating Frequency Distribution ----------
def run_job(mapper_script, reducer_script, input_file, output_file, sort_as_string=True):
    with open(input_file, "r", encoding="utf-8") as f:
        mapper_process = subprocess.run(
            ["python", mapper_script], stdin=f, capture_output=True, text=True
        )
    lines = mapper_process.stdout.strip().split("\n")

    if sort_as_string:
        sorted_lines = sorted(lines, key=lambda x: x.split("\t")[0])
    else:
        sorted_lines = sorted(lines, key=lambda x: int(x.split("\t")[0]))
    sorted_output = "\n".join(sorted_lines)

    reducer_process = subprocess.run(
        ["python", reducer_script], input=sorted_output, capture_output=True, text=True
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(reducer_process.stdout)
    print(f"Saved: {output_file} ({len(reducer_process.stdout.splitlines())} rows)")

print("\nRunning Job 2: Rating Frequency Distribution")
run_job(
    "mapper_rating_freq.py", "reducer_rating_freq.py",
    "../data/ratings.csv", f"{OUTPUT_DIR}/rating_frequency.csv"
)

print("\nRunning Job 3: Genre Movie Count")
run_job(
    "mapper_genre_count.py", "reducer_genre_count.py",
    "../data/movies.csv", f"{OUTPUT_DIR}/genre_movie_count.csv"
)