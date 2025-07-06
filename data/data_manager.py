# data_manager.py
# Handles all JSON read/write operations for movies and bookings 

import json
import os
from threading import Lock

class DataManager:
    _movies_file = os.path.join(os.path.dirname(__file__), 'movies.json')
    _bookings_file = os.path.join(os.path.dirname(__file__), 'bookings.json')
    _lock = Lock()

    @classmethod
    def load_movies(cls):
        with cls._lock:
            if not os.path.exists(cls._movies_file):
                return []
            with open(cls._movies_file, 'r', encoding='utf-8') as f:
                return json.load(f)

    @classmethod
    def save_movies(cls, movies):
        with cls._lock:
            with open(cls._movies_file, 'w', encoding='utf-8') as f:
                json.dump(movies, f, indent=2)

    @classmethod
    def load_bookings(cls):
        with cls._lock:
            if not os.path.exists(cls._bookings_file):
                return []
            with open(cls._bookings_file, 'r', encoding='utf-8') as f:
                return json.load(f)

    @classmethod
    def save_bookings(cls, bookings):
        with cls._lock:
            with open(cls._bookings_file, 'w', encoding='utf-8') as f:
                json.dump(bookings, f, indent=2) 