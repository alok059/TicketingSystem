# user_views.py
# User-side dialogs and windows for the Movie Ticket Booking System 
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QMessageBox, QGridLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from logic.booking_logic import BookingLogic
import os

class SeatSelectionDialog(QDialog):
    def __init__(self, movie_id, showtime_id, parent=None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.showtime_id = showtime_id
        self.selected_seats = []
        self.max_seats = 5
        self.seat_buttons = {}  # Store references to seat buttons
        self.init_ui()
        self.load_seats()
        self.load_styles()

    def load_styles(self):
        """Load QSS styles"""
        try:
            # Load main styles
            main_style_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.qss')
            seat_style_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'seat_buttons.qss')
            
            styles = ""
            
            # Load main styles
            if os.path.exists(main_style_file):
                with open(main_style_file, 'r', encoding='utf-8') as f:
                    styles += f.read()
            
            # Load seat button styles (these will override main styles)
            if os.path.exists(seat_style_file):
                with open(seat_style_file, 'r', encoding='utf-8') as f:
                    styles += "\n" + f.read()
            
            self.setStyleSheet(styles)
        except Exception as e:
            print(f"Error loading styles: {e}")

    def init_ui(self):
        self.setWindowTitle('Select Seats')
        self.setMinimumSize(700, 900)
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel(f'Select up to {self.max_seats} seats. Click seats to select/deselect.')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setProperty("class", "info")
        layout.addWidget(info_label)
        
        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel('Legend:'))
        
        available_label = QLabel('Available')
        available_label.setProperty("class", "legend-available")
        legend_layout.addWidget(available_label)
        
        selected_label = QLabel('Selected')
        selected_label.setProperty("class", "legend-selected")
        legend_layout.addWidget(selected_label)
        
        booked_label = QLabel('Booked')
        booked_label.setProperty("class", "legend-booked")
        legend_layout.addWidget(booked_label)
        
        legend_layout.addStretch()
        layout.addLayout(legend_layout)
        
        # Selected seats display
        self.selected_label = QLabel('Selected: None')
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setProperty("class", "info")
        layout.addWidget(self.selected_label)
        
        # Screen representation
        screen_frame = QFrame()
        screen_frame.setObjectName("screen")
        screen_frame.setFrameStyle(QFrame.Box)
        screen_frame.setMaximumHeight(60)
        screen_layout = QHBoxLayout()
        screen_label = QLabel('SCREEN')
        screen_label.setAlignment(Qt.AlignCenter)
        screen_layout.addWidget(screen_label)
        screen_frame.setLayout(screen_layout)
        layout.addWidget(screen_frame)
        
        # Seat grid
        self.seat_grid = QGridLayout()
        layout.addLayout(self.seat_grid)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.confirm_btn = QPushButton('Confirm Selection')
        self.confirm_btn.setObjectName("book_btn")
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setObjectName("cancel_btn")
        button_layout.addWidget(self.confirm_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.confirm_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def load_seats(self):
        all_seats = BookingLogic.get_all_seats(self.movie_id, self.showtime_id)
        available_seats = BookingLogic.get_available_seats(self.movie_id, self.showtime_id)
        
        # Clear existing buttons
        for i in reversed(range(self.seat_grid.count())):
            self.seat_grid.itemAt(i).widget().setParent(None)
        
        # Create seat buttons for all seats
        row_letters = sorted(set(seat[0] for seat in all_seats))
        
        # Optional: Create a mapping for custom row labels
        # Uncomment and modify the line below to change row labels
        # row_label_mapping = {'A': 'Front', 'B': 'Premium', 'C': 'Standard', 'D': 'Economy'}
        
        for row_idx, row_letter in enumerate(row_letters):
            # Row label
            # Use custom mapping if defined, otherwise use original letter
            display_label = row_letter
            # Uncomment the line below to use custom labels
            # display_label = row_label_mapping.get(row_letter, row_letter)
            
            row_label = QLabel(display_label)
            row_label.setAlignment(Qt.AlignCenter)
            row_label.setProperty("class", "row-label")
            self.seat_grid.addWidget(row_label, row_idx, 0)
            
            # Seat buttons for this row
            row_seats = [seat for seat in all_seats if seat.startswith(row_letter)]
            row_seats.sort(key=lambda x: int(x[1:]))
            
            for col_idx, seat in enumerate(row_seats):
                seat_btn = QPushButton(seat[1:])  # Show only the number
                seat_btn.setProperty('seat_id', seat)
                seat_btn.setProperty('class', 'seat')
                
                # Store reference to button
                self.seat_buttons[seat] = seat_btn
                
                # Set initial state based on availability
                if seat in available_seats:
                    seat_btn.setProperty('state', 'available')
                    seat_btn.clicked.connect(lambda checked, s=seat: self.toggle_seat(s))
                else:
                    # Booked seat
                    seat_btn.setProperty('state', 'booked')
                    seat_btn.setEnabled(False)
                
                self.seat_grid.addWidget(seat_btn, row_idx, col_idx + 1)

    def toggle_seat(self, seat_id):
        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
            # Reset button to available state
            if seat_id in self.seat_buttons:
                self.seat_buttons[seat_id].setProperty('state', 'available')
                self.seat_buttons[seat_id].style().unpolish(self.seat_buttons[seat_id])
                self.seat_buttons[seat_id].style().polish(self.seat_buttons[seat_id])
        else:
            if len(self.selected_seats) >= self.max_seats:
                QMessageBox.warning(self, 'Limit Reached', f'You can only select up to {self.max_seats} seats.')
                return
            self.selected_seats.append(seat_id)
            # Set button as selected (green)
            if seat_id in self.seat_buttons:
                self.seat_buttons[seat_id].setProperty('state', 'selected')
                self.seat_buttons[seat_id].style().unpolish(self.seat_buttons[seat_id])
                self.seat_buttons[seat_id].style().polish(self.seat_buttons[seat_id])
        
        self.update_selected_label()

    def update_selected_label(self):
        if self.selected_seats:
            self.selected_label.setText(f'Selected: {", ".join(sorted(self.selected_seats))}')
            self.selected_label.setProperty("class", "success")
        else:
            self.selected_label.setText('Selected: None')
            self.selected_label.setProperty("class", "info")

    def get_selected_seats(self):
        return self.selected_seats

class UserBookingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Book Tickets')
        self.setFixedSize(450, 450)
        self.load_styles()
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Book Your Movie Tickets')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "title")
        layout.addWidget(title_label)
        
        self.name_label = QLabel('Your Name:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your full name')
        
        self.movie_label = QLabel('Select Movie:')
        self.movie_combo = QComboBox()
        
        self.showtime_label = QLabel('Select Showtime:')
        self.showtime_combo = QComboBox()
        
        self.select_seats_btn = QPushButton('Select Seats')
        self.select_seats_btn.setObjectName("book_btn")
        
        self.book_btn = QPushButton('Book Tickets')
        self.book_btn.setObjectName("book_btn")
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.movie_label)
        layout.addWidget(self.movie_combo)
        layout.addWidget(self.showtime_label)
        layout.addWidget(self.showtime_combo)
        layout.addWidget(self.select_seats_btn)
        layout.addWidget(self.book_btn)
        
        self.setLayout(layout)
        self.populate_movies()
        self.movie_combo.currentIndexChanged.connect(self.populate_showtimes)
        self.select_seats_btn.clicked.connect(self.open_seat_selection)
        self.book_btn.clicked.connect(self.book_tickets)
        
        self.selected_seats = []
        self.user_id = None

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

    def populate_movies(self):
        self.movie_combo.clear()
        self.movies = BookingLogic.get_movies()
        for movie in self.movies:
            self.movie_combo.addItem(movie['title'], movie['id'])
        self.populate_showtimes()

    def populate_showtimes(self):
        self.showtime_combo.clear()
        idx = self.movie_combo.currentIndex()
        if idx < 0 or not self.movies:
            return
        movie_id = self.movies[idx]['id']
        showtimes = BookingLogic.get_showtimes(movie_id)
        for show in showtimes:
            self.showtime_combo.addItem(show['time'], show['id'])

    def open_seat_selection(self):
        idx = self.movie_combo.currentIndex()
        showtime_idx = self.showtime_combo.currentIndex()
        if idx < 0 or showtime_idx < 0:
            QMessageBox.warning(self, 'Error', 'Please select a movie and showtime first.')
            return
        
        movie_id = self.movies[idx]['id']
        showtime_id = BookingLogic.get_showtimes(movie_id)[showtime_idx]['id']
        
        dialog = SeatSelectionDialog(movie_id, showtime_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.selected_seats = dialog.get_selected_seats()
            if self.selected_seats:
                self.select_seats_btn.setText(f'Seats: {", ".join(self.selected_seats)}')
            else:
                self.select_seats_btn.setText('Select Seats')

    def book_tickets(self):
        name = self.name_input.text().strip()
        movie_idx = self.movie_combo.currentIndex()
        showtime_idx = self.showtime_combo.currentIndex()
        
        if not name or movie_idx < 0 or showtime_idx < 0 or not self.selected_seats:
            QMessageBox.warning(self, 'Error', 'Please fill all fields and select seats.')
            return
        
        movie_id = self.movies[movie_idx]['id']
        showtime_id = BookingLogic.get_showtimes(movie_id)[showtime_idx]['id']
        
        if not BookingLogic.are_seats_available(movie_id, showtime_id, self.selected_seats):
            QMessageBox.warning(self, 'Error', 'One or more selected seats are not available.')
            return
        
        booking_result = BookingLogic.book_seats(name, movie_id, showtime_id, self.selected_seats)
        if booking_result:
            booking_ids, user_id = booking_result
            self.user_id = user_id
            QMessageBox.information(self, 'Success', 
                                  f'Booking successful! Your ticket IDs: {", ".join(booking_ids)}\n\n'
                                  f'User ID: {user_id[:8]}... (save this for cancellation)')
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Booking failed. Seats may already be booked.')

    def get_user_id(self):
        return self.user_id

class UserCancelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cancel Booking')
        self.setFixedSize(450, 450)
        self.load_styles()
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Cancel Your Booking')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "title")
        layout.addWidget(title_label)
        
        # Booking ID option
        self.id_label = QLabel('Booking ID (optional):')
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('Enter specific booking ID')
        
        # User ID option (recommended)
        self.user_id_label = QLabel('User ID (recommended):')
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText('Enter your User ID from booking confirmation')
        
        # Name option (legacy)
        self.name_label = QLabel('Or Your Name (legacy):')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your name (may affect others with same name)')
        
        # Info text
        info_label = QLabel('Note: Use User ID for precise cancellation. Name-based cancellation may affect others with the same name.')
        info_label.setProperty("class", "warning")
        info_label.setWordWrap(True)
        
        self.cancel_btn = QPushButton('Cancel Booking')
        self.cancel_btn.setObjectName("cancel_btn")
        
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(info_label)
        layout.addWidget(self.cancel_btn)
        
        self.setLayout(layout)
        self.cancel_btn.clicked.connect(self.cancel_booking)

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

    def cancel_booking(self):
        booking_id = self.id_input.text().strip()
        user_id = self.user_id_input.text().strip()
        user_name = self.name_input.text().strip()
        
        if not booking_id and not user_id and not user_name:
            QMessageBox.warning(self, 'Error', 'Please enter Booking ID, User ID, or Name.')
            return
        
        # Priority: Booking ID > User ID > Name
        if booking_id:
            result = BookingLogic.cancel_booking(booking_id=booking_id)
            message = f'Booking {booking_id[:8]}... cancelled.'
        elif user_id:
            # Check how many bookings will be cancelled
            user_bookings = BookingLogic.get_user_bookings(user_id)
            if not user_bookings:
                QMessageBox.warning(self, 'Error', 'No bookings found for this User ID.')
                return
            
            num_bookings = len(user_bookings)
            seats = [b['seat'] for b in user_bookings]
            seats_str = ", ".join(sorted(seats))
            
            reply = QMessageBox.question(self, 'Confirm Cancellation', 
                                       f'This will cancel {num_bookings} booking(s) for seats: {seats_str}\n\nAre you sure?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            result = BookingLogic.cancel_user_bookings(user_id)
            message = f'All {num_bookings} booking(s) for User ID {user_id[:8]}... cancelled.'
        else:
            # Check how many bookings will be cancelled for this name
            all_bookings = BookingLogic.get_bookings()
            name_bookings = [b for b in all_bookings if b['user_name'] == user_name]
            if not name_bookings:
                QMessageBox.warning(self, 'Error', 'No bookings found for this name.')
                return
            
            num_bookings = len(name_bookings)
            seats = [b['seat'] for b in name_bookings]
            seats_str = ", ".join(sorted(seats))
            
            reply = QMessageBox.question(self, 'Confirm Cancellation', 
                                       f'This will cancel {num_bookings} booking(s) for "{user_name}" with seats: {seats_str}\n\nAre you sure?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            result = BookingLogic.cancel_booking(user_name=user_name)
            message = f'All {num_bookings} booking(s) for "{user_name}" cancelled.'
        
        if result:
            QMessageBox.information(self, 'Success', message)
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'No matching booking found.') 