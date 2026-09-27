"""
mapper_rating_freq.py
Emits (rating_value, 1) — we're counting how often each rating value occurs.
"""

import sys

for line_no, line in enumerate(sys.stdin):
    line = line.strip()
    if not line or line_no == 0:
        continue
    parts = line.split(",")
    rating = parts[2].strip()  # e.g. "4.0"
    print(f"{rating}\t1")