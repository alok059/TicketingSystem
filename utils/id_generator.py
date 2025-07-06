# id_generator.py
# Utility for generating short IDs instead of long UUIDs

import random
import string
import time

def generate_short_id(prefix=""):
    """
    Generate a short 8-character ID.
    Optionally accepts a prefix to make IDs more descriptive.
    """
    # Use timestamp for uniqueness
    timestamp = str(int(time.time() * 1000))[-4:]  # Last 4 digits of timestamp
    
    # Generate random characters
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # Combine timestamp and random chars
    short_id = timestamp + random_chars
    
    # Add prefix if provided
    if prefix:
        short_id = prefix + short_id
    
    return short_id

def generate_movie_id():
    """Generate a short movie ID"""
    return generate_short_id("M")

def generate_showtime_id():
    """Generate a short showtime ID"""
    return generate_short_id("S")

def generate_user_id():
    """Generate a short user ID"""
    return generate_short_id("U")

def generate_booking_id():
    """Generate a short booking ID"""
    return generate_short_id("B") 