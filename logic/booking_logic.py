# booking_logic.py
# Booking, seat selection, and cancellation logic for the Movie Ticket Booking System 

from data.data_manager import DataManager
from utils.id_generator import generate_user_id, generate_booking_id

class BookingLogic:
    @staticmethod
    def get_movies():
        return DataManager.load_movies()

    @staticmethod
    def get_showtimes(movie_id):
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                return movie.get('showtimes', [])
        return []

    @staticmethod
    def is_seat_available(movie_id, showtime_id, seat):
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                for showtime in movie.get('showtimes', []):
                    if showtime['id'] == showtime_id:
                        return seat in showtime.get('available_seats', [])
        return False

    @staticmethod
    def are_seats_available(movie_id, showtime_id, seats):
        """Check if multiple seats are available"""
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                for showtime in movie.get('showtimes', []):
                    if showtime['id'] == showtime_id:
                        available_seats = showtime.get('available_seats', [])
                        return all(seat in available_seats for seat in seats)
        return False

    @staticmethod
    def book_seats(user_name, movie_id, showtime_id, seats):
        """Book multiple seats at once"""
        if len(seats) > 5:
            return None  # Maximum 5 seats per booking
        
        movies = DataManager.load_movies()
        bookings = DataManager.load_bookings()
        
        # Generate unique user ID
        user_id = generate_user_id()
        
        for movie in movies:
            if movie['id'] == movie_id:
                for showtime in movie.get('showtimes', []):
                    if showtime['id'] == showtime_id:
                        available_seats = showtime.get('available_seats', [])
                        # Check if all seats are available
                        if not all(seat in available_seats for seat in seats):
                            return None
                        
                        # Remove seats from available
                        for seat in seats:
                            available_seats.remove(seat)
                        
                        # Create booking for each seat
                        booking_ids = []
                        for seat in seats:
                            booking_id = generate_booking_id()
                            booking = {
                                'id': booking_id,
                                'user_id': user_id,
                                'user_name': user_name,
                                'movie_id': movie_id,
                                'showtime_id': showtime_id,
                                'seat': seat
                            }
                            bookings.append(booking)
                            booking_ids.append(booking_id)
                        
                        DataManager.save_movies(movies)
                        DataManager.save_bookings(bookings)
                        return (booking_ids, user_id)
        return None

    @staticmethod
    def book_seat(user_name, movie_id, showtime_id, seat):
        """Legacy method for single seat booking"""
        result = BookingLogic.book_seats(user_name, movie_id, showtime_id, [seat])
        return result[0][0] if result else None

    @staticmethod
    def cancel_booking(booking_id=None, user_name=None, user_id=None):
        """
        Cancel booking(s) based on provided criteria.
        - If booking_id: Cancel specific booking
        - If user_id: Cancel ALL bookings for that user
        - If user_name: Cancel ALL bookings for that user (legacy)
        """
        bookings = DataManager.load_bookings()
        movies = DataManager.load_movies()
        
        if booking_id:
            # Cancel specific booking by ID
            booking_to_cancel = None
            for booking in bookings:
                if booking['id'] == booking_id:
                    booking_to_cancel = booking
                    break
            
            if not booking_to_cancel:
                return False
            
            # Restore seat
            for movie in movies:
                if movie['id'] == booking_to_cancel['movie_id']:
                    for showtime in movie.get('showtimes', []):
                        if showtime['id'] == booking_to_cancel['showtime_id']:
                            showtime['available_seats'].append(booking_to_cancel['seat'])
                            break
            
            # Remove the booking
            bookings.remove(booking_to_cancel)
            DataManager.save_movies(movies)
            DataManager.save_bookings(bookings)
            return True
            
        elif user_id:
            # Cancel ALL bookings for specific user ID
            return BookingLogic.cancel_user_bookings(user_id)
            
        elif user_name:
            # Cancel ALL bookings for user name (legacy support)
            user_bookings = [b for b in bookings if b['user_name'] == user_name]
            
            if not user_bookings:
                return False
            
            # Restore all seats for this user
            for booking in user_bookings:
                for movie in movies:
                    if movie['id'] == booking['movie_id']:
                        for showtime in movie.get('showtimes', []):
                            if showtime['id'] == booking['showtime_id']:
                                showtime['available_seats'].append(booking['seat'])
                                break
            
            # Remove all bookings for this user
            bookings = [b for b in bookings if b['user_name'] != user_name]
            DataManager.save_movies(movies)
            DataManager.save_bookings(bookings)
            return True
        
        return False

    @staticmethod
    def cancel_user_bookings(user_id):
        """Cancel all bookings for a specific user ID"""
        bookings = DataManager.load_bookings()
        movies = DataManager.load_movies()
        user_bookings = [b for b in bookings if b.get('user_id') == user_id]
        
        if not user_bookings:
            return False
            
        # Restore all seats for this user
        for booking in user_bookings:
            for movie in movies:
                if movie['id'] == booking['movie_id']:
                    for showtime in movie.get('showtimes', []):
                        if showtime['id'] == booking['showtime_id']:
                            showtime['available_seats'].append(booking['seat'])
                            break
        
        # Remove all bookings for this user
        bookings = [b for b in bookings if b.get('user_id') != user_id]
        DataManager.save_movies(movies)
        DataManager.save_bookings(bookings)
        return True

    @staticmethod
    def get_bookings():
        return DataManager.load_bookings()

    @staticmethod
    def get_user_bookings(user_id):
        """Get all bookings for a specific user ID"""
        bookings = DataManager.load_bookings()
        return [b for b in bookings if b.get('user_id') == user_id]

    @staticmethod
    def get_available_seats(movie_id, showtime_id):
        """Get list of available seats for a showtime"""
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                for showtime in movie.get('showtimes', []):
                    if showtime['id'] == showtime_id:
                        return showtime.get('available_seats', [])
        return []

    @staticmethod
    def get_all_seats(movie_id, showtime_id):
        """Get all seats (both available and booked) for a showtime"""
        movies = DataManager.load_movies()
        for movie in movies:
            if movie['id'] == movie_id:
                for showtime in movie.get('showtimes', []):
                    if showtime['id'] == showtime_id:
                        # Get all seats that were originally created for this showtime
                        # We need to reconstruct this from the seat pattern
                        available_seats = showtime.get('available_seats', [])
                        booked_seats = []
                        
                        # Get booked seats from bookings
                        bookings = DataManager.load_bookings()
                        for booking in bookings:
                            if booking['movie_id'] == movie_id and booking['showtime_id'] == showtime_id:
                                booked_seats.append(booking['seat'])
                        
                        # Combine and sort all seats
                        all_seats = available_seats + booked_seats
                        return sorted(all_seats, key=lambda x: (x[0], int(x[1:])))
        return [] 