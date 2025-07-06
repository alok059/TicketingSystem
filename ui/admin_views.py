# admin_views.py
# Admin-side dialogs and windows for the Movie Ticket Booking System 
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QListWidget, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from logic.admin_logic import AdminLogic
import os

class AdminLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Login')
        self.setFixedSize(350, 250)
        self.load_styles()
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Admin Authentication')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "title")
        layout.addWidget(title_label)
        
        self.user_label = QLabel('Username:')
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('Enter admin username')
        
        self.pass_label = QLabel('Password:')
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText('Enter admin password')
        self.pass_input.setEchoMode(QLineEdit.Password)
        
        self.login_btn = QPushButton('Login')
        self.login_btn.setObjectName("admin_btn")
        
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.login_btn.clicked.connect(self.try_login)

    def load_styles(self):
        """Load QSS styles"""
        try:
            style_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.qss')
            with open(style_file, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Style file not found at {style_file}")
        except Exception as e:
            print(f"Error loading styles: {e}")

    def try_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        if AdminLogic.login(username, password):
            self.accept()
            panel = AdminPanelDialog()
            panel.exec_()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid admin credentials.')

class AdminPanelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Panel')
        self.setMinimumSize(700, 900)
        self.load_styles()
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Movie Management Panel')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "title")
        layout.addWidget(title_label)
        
        # Add Movie Section
        movie_group = QGroupBox('Add New Movie')
        movie_layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Movie Title')
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText('Description')
        self.dur_input = QLineEdit()
        self.dur_input.setPlaceholderText('Duration (minutes)')
        self.add_movie_btn = QPushButton('Add Movie')
        self.add_movie_btn.setObjectName("book_btn")
        movie_layout.addWidget(self.title_input)
        movie_layout.addWidget(self.desc_input)
        movie_layout.addWidget(self.dur_input)
        movie_layout.addWidget(self.add_movie_btn)
        movie_group.setLayout(movie_layout)
        layout.addWidget(movie_group)
        
        # Remove Movie Section
        remove_group = QGroupBox('Remove Movie')
        remove_layout = QVBoxLayout()
        self.movie_combo = QComboBox()
        self.remove_movie_btn = QPushButton('Remove Selected Movie')
        self.remove_movie_btn.setObjectName("cancel_btn")
        remove_layout.addWidget(self.movie_combo)
        remove_layout.addWidget(self.remove_movie_btn)
        remove_group.setLayout(remove_layout)
        layout.addWidget(remove_group)
        
        # Add Showtime Section
        showtime_group = QGroupBox('Add Showtime')
        showtime_layout = QVBoxLayout()
        showtime_info = QLabel('Note: Seats will be automatically set to multiples of 10')
        showtime_info.setProperty("class", "info")
        self.showtime_input = QLineEdit()
        self.showtime_input.setPlaceholderText('Showtime (e.g. 18:00)')
        self.seats_input = QLineEdit()
        self.seats_input.setPlaceholderText('Total Seats (will be rounded to nearest 10)')
        self.add_showtime_btn = QPushButton('Add Showtime')
        self.add_showtime_btn.setObjectName("book_btn")
        showtime_layout.addWidget(showtime_info)
        showtime_layout.addWidget(self.showtime_input)
        showtime_layout.addWidget(self.seats_input)
        showtime_layout.addWidget(self.add_showtime_btn)
        showtime_group.setLayout(showtime_layout)
        layout.addWidget(showtime_group)
        
        # View Bookings Section
        bookings_group = QGroupBox('View All Bookings')
        bookings_layout = QVBoxLayout()
        self.view_bookings_btn = QPushButton('Refresh Bookings')
        self.view_bookings_btn.setObjectName("admin_btn")
        self.bookings_list = QListWidget()
        bookings_layout.addWidget(self.view_bookings_btn)
        bookings_layout.addWidget(self.bookings_list)
        bookings_group.setLayout(bookings_layout)
        layout.addWidget(bookings_group)
        
        self.setLayout(layout)
        self.add_movie_btn.clicked.connect(self.add_movie)
        self.remove_movie_btn.clicked.connect(self.remove_movie)
        self.add_showtime_btn.clicked.connect(self.add_showtime)
        self.view_bookings_btn.clicked.connect(self.view_bookings)
        self.refresh_movies()

    def load_styles(self):
        """Load QSS styles"""
        try:
            style_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.qss')
            with open(style_file, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Style file not found at {style_file}")
        except Exception as e:
            print(f"Error loading styles: {e}")

    def refresh_movies(self):
        self.movie_combo.clear()
        from data.data_manager import DataManager
        self.movies = DataManager.load_movies()
        for movie in self.movies:
            self.movie_combo.addItem(movie['title'], movie['id'])

    def add_movie(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.text().strip()
        dur = self.dur_input.text().strip()
        if not title or not desc or not dur:
            QMessageBox.warning(self, 'Error', 'Fill all movie fields.')
            return
        try:
            int(dur)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Duration must be a number.')
            return
        AdminLogic.add_movie(title, desc, dur)
        QMessageBox.information(self, 'Success', 'Movie added successfully.')
        self.title_input.clear()
        self.desc_input.clear()
        self.dur_input.clear()
        self.refresh_movies()

    def remove_movie(self):
        idx = self.movie_combo.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, 'Error', 'Please select a movie to remove.')
            return
        movie_id = self.movie_combo.itemData(idx)
        movie_title = self.movie_combo.currentText()
        reply = QMessageBox.question(self, 'Confirm Removal', 
                                   f'Are you sure you want to remove "{movie_title}"?',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            AdminLogic.remove_movie(movie_id)
            QMessageBox.information(self, 'Success', 'Movie removed successfully.')
            self.refresh_movies()

    def add_showtime(self):
        idx = self.movie_combo.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, 'Error', 'Please select a movie first.')
            return
        movie_id = self.movie_combo.itemData(idx)
        time = self.showtime_input.text().strip()
        try:
            seats = int(self.seats_input.text().strip())
            if seats <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Seats must be a positive number.')
            return
        
        # Show user the actual number of seats that will be created
        actual_seats = ((seats // 10) + 1) * 10 if seats % 10 != 0 else seats
        if actual_seats != seats:
            reply = QMessageBox.question(self, 'Seat Adjustment', 
                                       f'Seats will be adjusted to {actual_seats} (nearest multiple of 10). Continue?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        AdminLogic.add_showtime(movie_id, time, seats)
        QMessageBox.information(self, 'Success', f'Showtime added with {actual_seats} seats.')
        self.showtime_input.clear()
        self.seats_input.clear()

    def view_bookings(self):
        self.bookings_list.clear()
        bookings = AdminLogic.get_all_bookings()
        
        if not bookings:
            self.bookings_list.addItem('No bookings found.')
            return
        
        # Group bookings by user ID (unique user)
        user_bookings = {}
        for booking in bookings:
            user_id = booking.get('user_id', 'legacy')  # Handle legacy bookings without user_id
            if user_id not in user_bookings:
                user_bookings[user_id] = []
            user_bookings[user_id].append(booking)
        
        # Create movie ID to name mapping
        movie_names = {movie['id']: movie['title'] for movie in self.movies}
        
        # Display grouped bookings
        for user_id, user_booking_list in user_bookings.items():
            # Get user name from first booking
            user_name = user_booking_list[0]['user_name']
            
            # Group by movie and showtime
            movie_showtime_bookings = {}
            for booking in user_booking_list:
                key = (booking['movie_id'], booking['showtime_id'])
                if key not in movie_showtime_bookings:
                    movie_showtime_bookings[key] = []
                movie_showtime_bookings[key].append(booking)
            
            # Display each movie/showtime combination for this user
            for (movie_id, showtime_id), seat_bookings in movie_showtime_bookings.items():
                movie_name = movie_names.get(movie_id, "Unknown Movie")
                seats = [booking['seat'] for booking in seat_bookings]
                seats_str = ", ".join(sorted(seats))
                booking_ids = [booking['id'][:8] + "..." for booking in seat_bookings]
                ids_str = ", ".join(booking_ids)
                
                # Show user ID if available
                user_display = f"{user_name} (ID: {user_id[:8]}...)" if user_id != 'legacy' else user_name
                
                display_text = f"User: {user_display} | Movie: {movie_name} | Seats: {seats_str} | Booking IDs: {ids_str}"
                self.bookings_list.addItem(display_text) 