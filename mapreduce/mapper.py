"""
mapper.py
MAP phase: reads ratings.csv line by line, emits (movie_id, rating) pairs.
This mimics Hadoop Streaming's mapper contract: read stdin, write stdout,
tab-separated key-value pairs.
"""

import sys

for line_no, line in enumerate(sys.stdin):
    line = line.strip()
    if not line or line_no == 0:  # skip header row
        continue
    parts = line.split(",")
    # ratings.csv columns: user_id,movie_id,rating,timestamp
    movie_id = parts[1].strip()
    rating = parts[2].strip()
    print(f"{movie_id}\t{rating}")