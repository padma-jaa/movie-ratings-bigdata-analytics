"""
generate_dataset.py
Generates synthetic movie ratings data: movies.csv, users.csv, ratings.csv
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)  # reproducible results

# ---------- CONFIG ----------
NUM_MOVIES = 500
NUM_USERS = 1000
NUM_RATINGS = 50000

GENRES = ["Action", "Comedy", "Drama", "Thriller", "Romance", "Sci-Fi",
          "Horror", "Animation", "Documentary", "Adventure", "Fantasy",
          "Crime", "Biography", "Mystery", "Musical"]

CITIES = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad",
          "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]

OCCUPATIONS = ["Student", "Engineer", "Doctor", "Teacher", "Artist",
               "Manager", "Researcher", "Lawyer", "Nurse", "Designer"]

# ---------- 1. GENERATE MOVIES ----------
def generate_movies():
    movies = []
    for movie_id in range(1, NUM_MOVIES + 1):
        title = f"Movie Title {movie_id}"
        num_genres = random.randint(1, 3)
        genres = "|".join(random.sample(GENRES, num_genres))
        year = random.randint(2000, 2024)
        movies.append([movie_id, title, genres, year])
    return movies

# ---------- 2. GENERATE USERS ----------
def generate_users():
    users = []
    for user_id in range(1, NUM_USERS + 1):
        age = random.randint(15, 65)
        gender = random.choice(["M", "F", "Other"])
        occupation = random.choice(OCCUPATIONS)
        city = random.choice(CITIES)
        users.append([user_id, age, gender, occupation, city])
    return users

# ---------- 3. GENERATE RATINGS ----------
def generate_ratings():
    ratings = []
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    possible_ratings = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    for _ in range(NUM_RATINGS):
        user_id = random.randint(1, NUM_USERS)
        movie_id = random.randint(1, NUM_MOVIES)
        rating = random.choice(possible_ratings)
        random_days = random.randint(0, date_range_days)
        timestamp = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        ratings.append([user_id, movie_id, rating, timestamp])
    return ratings

# ---------- WRITE TO CSV ----------
def write_csv(filename, header, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Saved: {filename} ({len(rows)} rows)")

if __name__ == "__main__":
    movies = generate_movies()
    users = generate_users()
    ratings = generate_ratings()

    write_csv("movies.csv", ["movie_id", "title", "genres", "year"], movies)
    write_csv("users.csv", ["user_id", "age", "gender", "occupation", "city"], users)
    write_csv("ratings.csv", ["user_id", "movie_id", "rating", "timestamp"], ratings)

    print("\nDataset generation complete.")