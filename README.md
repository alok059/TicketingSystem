# Movie Ticket Booking System

A desktop-based movie ticket booking application built with Python and PyQt5, featuring a graphical user interface for both users and administrators with modern styling and comprehensive functionality.

## Features

### 👤 User Features
- **Browse Movies**: View all available movies with descriptions and durations
- **Select Showtimes**: Choose from available showtimes for each movie
- **Graphical Seat Selection**: Interactive seat map allowing selection of up to 5 seats
- **Book Tickets**: Reserve multiple seats with a single booking
- **Cancel Bookings**: Cancel existing bookings using booking ID or user name
- **Modern UI**: Beautiful and responsive interface with custom styling

### 🛠️ Admin Features
- **Secure Login**: Admin authentication with hardcoded credentials
- **Movie Management**: Add new movies with title, description, and duration
- **Remove Movies**: Delete movies from the system
- **Showtime Management**: Add showtimes with automatic seat allocation (multiples of 10)
- **View Bookings**: See all current bookings with user details
- **Data Management**: Tools for data regeneration and maintenance

## Technical Specifications

- **Language**: Python 3.x
- **GUI Framework**: PyQt5
- **Data Storage**: JSON files (movies.json, bookings.json)
- **Architecture**: Modular design with separate layers for UI, logic, and data
- **Styling**: Custom QSS (Qt Style Sheets) for modern appearance
- **Seat System**: Automatic seat allocation in multiples of 10 (A1-A10, B1-B10, etc.)

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd TicketingSystem
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Running the Application
```bash
python main.py
```

### Admin Login
- **Username**: `admin`
- **Password**: `admin`

### User Booking Process
1. Click "Book Ticket" from the main window
2. Enter your name
3. Select a movie from the dropdown
4. Choose a showtime
5. Click "Select Seats" to open the graphical seat map
6. Click on seats to select (up to 5 seats maximum)
7. Click "Confirm Selection" to proceed
8. Click "Book Tickets" to complete the booking

### Admin Operations
1. Click "Admin" from the main window
2. Enter admin credentials
3. Use the admin panel to:
   - Add new movies with details
   - Remove existing movies
   - Add showtimes (seats automatically set to multiples of 10)
   - View all current bookings

### Data Management
- Use `utils/regenerate_data.py` to reset or regenerate sample data
- The system automatically generates unique IDs for movies, showtimes, and bookings

## Project Structure

```
TicketingSystem/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── ui/                    # User interface components
│   ├── main_window.py     # Main application window
│   ├── user_views.py      # User booking and cancellation dialogs
│   └── admin_views.py     # Admin login and management dialogs
├── logic/                 # Business logic
│   ├── booking_logic.py   # Booking and seat management
│   └── admin_logic.py     # Admin operations
├── data/                  # Data storage
│   ├── data_manager.py    # JSON file operations
│   ├── movies.json        # Movie and showtime data
│   └── bookings.json      # Booking records
├── styles/                # UI styling
│   ├── main.qss          # Main application styles
│   └── seat_buttons.qss  # Seat selection button styles
└── utils/                 # Utility functions
    ├── validators.py      # Input validation
    ├── id_generator.py    # Unique ID generation
    └── regenerate_data.py # Data regeneration utilities
```

## Data Format

### Movies JSON Structure
```json
[
  {
    "id": "unique-movie-id",
    "title": "Movie Title",
    "description": "Movie description",
    "duration": "120",
    "showtimes": [
      {
        "id": "unique-showtime-id",
        "time": "18:00",
        "available_seats": ["A1", "A2", "A3", ...]
      }
    ]
  }
]
```

### Bookings JSON Structure
```json
[
  {
    "id": "unique-booking-id",
    "user_name": "User Name",
    "movie_id": "movie-id",
    "showtime_id": "showtime-id",
    "seat": "A1"
  }
]
```

## Features in Detail

### Seat Selection System
- **Graphical Interface**: Visual seat map with clickable buttons
- **Multiple Selection**: Users can select up to 5 seats per booking
- **Real-time Updates**: Selected seats are highlighted in green
- **Automatic Validation**: Prevents double-booking and invalid selections
- **Custom Styling**: Beautiful seat buttons with hover effects

### Seat Allocation
- **Multiples of 10**: All showtimes automatically have seats in multiples of 10
- **Row-based System**: Seats organized in rows (A, B, C, D, E, etc.)
- **Numbered Seats**: Each row has seats numbered 1-10

### Data Persistence
- **JSON Storage**: All data stored in human-readable JSON files
- **Atomic Operations**: Thread-safe file operations with locks
- **Automatic Backup**: Data persists between application sessions
- **Data Regeneration**: Tools available to reset or regenerate sample data

### User Interface
- **Modern Design**: Clean and intuitive interface with custom styling
- **Responsive Layout**: Adapts to different window sizes
- **Visual Feedback**: Clear indicators for user actions and system states
- **Accessibility**: Easy-to-use controls and clear navigation





