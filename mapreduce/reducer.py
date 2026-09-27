"""
reducer.py
REDUCE phase: receives (movie_id, rating) pairs SORTED by movie_id
(the "shuffle" step sorts them before they reach us).
Aggregates count and average rating per movie.
"""

import sys

current_movie = None
total_rating = 0.0
count = 0

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    movie_id, rating = parts[0], float(parts[1])

    if current_movie == movie_id:
        total_rating += rating
        count += 1
    else:
        if current_movie is not None:
            avg = total_rating / count
            print(f"{current_movie}\t{count}\t{avg:.4f}")
        current_movie = movie_id
        total_rating = rating
        count = 1

# don't forget the last group
if current_movie is not None:
    avg = total_rating / count
    print(f"{current_movie}\t{count}\t{avg:.4f}")