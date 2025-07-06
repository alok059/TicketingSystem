# regenerate_data.py
# Script to regenerate data files with short IDs

import json
import os
from id_generator import generate_movie_id, generate_showtime_id, generate_user_id, generate_booking_id

def regenerate_movies_data():
    """Regenerate movies.json with short IDs"""
    
    # Sample movies data with short IDs
    movies = [
        {
            "id": generate_movie_id(),
            "title": "The Shawshank Redemption",
            "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "duration": "142",
            "showtimes": [
                {
                    "id": generate_showtime_id(),
                    "time": "14:00",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(10) for j in range(1, 11)]
                },
                {
                    "id": generate_showtime_id(),
                    "time": "17:30",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(10) for j in range(1, 11)]
                },
                {
                    "id": generate_showtime_id(),
                    "time": "21:00",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(10) for j in range(1, 11)]
                }
            ]
        },
        {
            "id": generate_movie_id(),
            "title": "The Godfather",
            "description": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
            "duration": "175",
            "showtimes": [
                {
                    "id": generate_showtime_id(),
                    "time": "15:00",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(8) for j in range(1, 11)]
                },
                {
                    "id": generate_showtime_id(),
                    "time": "19:00",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(8) for j in range(1, 11)]
                }
            ]
        },
        {
            "id": generate_movie_id(),
            "title": "Pulp Fiction",
            "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine.",
            "duration": "154",
            "showtimes": [
                {
                    "id": generate_showtime_id(),
                    "time": "16:30",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(12) for j in range(1, 11)]
                },
                {
                    "id": generate_showtime_id(),
                    "time": "20:30",
                    "available_seats": [f"{chr(65+i)}{j}" for i in range(12) for j in range(1, 11)]
                }
            ]
        }
    ]
    
    # Save to movies.json
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    movies_file = os.path.join(data_dir, 'movies.json')
    
    with open(movies_file, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    
    print(f"Regenerated movies.json with short IDs")
    print(f"Generated {len(movies)} movies with {sum(len(m['showtimes']) for m in movies)} showtimes")

def regenerate_bookings_data():
    """Regenerate bookings.json with short IDs"""
    
    # Start with empty bookings
    bookings = []
    
    # Save to bookings.json
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    bookings_file = os.path.join(data_dir, 'bookings.json')
    
    with open(bookings_file, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, indent=2, ensure_ascii=False)
    
    print(f"Regenerated bookings.json with short IDs")
    print(f"Generated {len(bookings)} bookings")

if __name__ == "__main__":
    print("Regenerating data files with short IDs...")
    regenerate_movies_data()
    regenerate_bookings_data()
    print("Data regeneration complete!") 