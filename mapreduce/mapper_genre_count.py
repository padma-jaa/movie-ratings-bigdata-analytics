"""
mapper_genre_count.py
Reads movies.csv, splits pipe-separated genres, emits (genre, 1) per genre
per movie.
"""

import sys

for line_no, line in enumerate(sys.stdin):
    line = line.strip()
    if not line or line_no == 0:
        continue
    parts = line.split(",")
    genres_field = parts[2].strip()  # movies.csv: movie_id,title,genres,year
    for genre in genres_field.split("|"):
        print(f"{genre}\t1")