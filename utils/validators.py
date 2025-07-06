# validators.py
# Input validation and helper functions for the Movie Ticket Booking System 

import re

def validate_non_empty(value):
    return bool(value and str(value).strip())

def validate_seat_format(seat):
    return bool(re.match(r'^[A-E][1-9][0-9]*$', seat))

def validate_duration(duration):
    try:
        d = int(duration)
        return d > 0
    except (ValueError, TypeError):
        return False 