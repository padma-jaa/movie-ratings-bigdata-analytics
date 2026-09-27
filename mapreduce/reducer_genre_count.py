"""
reducer_rating_freq.py
Sums up counts per rating value (sorted input assumed).
"""

import sys

current_rating = None
count = 0

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    rating, val = parts[0], int(parts[1])

    if current_rating == rating:
        count += val
    else:
        if current_rating is not None:
            print(f"{current_rating}\t{count}")
        current_rating = rating
        count = val

if current_rating is not None:
    print(f"{current_rating}\t{count}")