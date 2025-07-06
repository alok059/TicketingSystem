# admin_logic.py
# Admin movie/showtime management logic for the Movie Ticket Booking System 

from data.data_manager import DataManager
from utils.id_generator import generate_movie_id, generate_showtime_id

class AdminLogic:
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin'  # Hardcoded credentials

    @staticmethod
    def login(username, password):
        return username == AdminLogic.ADMIN_USERNAME and password == AdminLogic.ADMIN_PASSWORD

    @staticmethod
    def add_movie(title, description, duration):
        movies = DataManager.load_movies()
        movie_id = generate_movie_id()
        movie = {
            'id': movie_id,
            'title': title,
            'description': description,
            'duration': duration,
            'showtimes': []
        }
        movies.append(movie)
        DataManager.save_movies(movies)
        return movie_id

    @staticmethod
    def remove_movie(movie_id):
        movies = DataManager.load_movies()
        movies = [m for m in movies if m['id'] != movie_id]
        DataManager.save_movies(movies)

    @staticmethod
    def add_showtime(movie_id, time, total_seats):
        # Ensure seats are in multiples of 10
        if total_seats % 10 != 0:
            total_seats = ((total_seats // 10) + 1) * 10
        
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                showtime_id = generate_showtime_id()
                # Generate seats in format A1-A10, B1-B10, etc.
                available_seats = []
                rows = total_seats // 10
                for row in range(rows):
                    row_letter = chr(65 + row)  # A, B, C, D, E, etc.
                    for seat_num in range(1, 11):
                        available_seats.append(f"{row_letter}{seat_num}")
                
                showtime = {
                    'id': showtime_id,
                    'time': time,
                    'available_seats': available_seats
                }
                movie['showtimes'].append(showtime)
                DataManager.save_movies(movies)
                return showtime_id
        return None

    @staticmethod
    def get_all_bookings():
        return DataManager.load_bookings() 