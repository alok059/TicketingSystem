# main_window.py
# Main window and navigation for the Movie Ticket Booking System 
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
import sys
import os
from ui.user_views import UserBookingDialog, UserCancelDialog
from ui.admin_views import AdminLoginDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Movie Ticket Booking System')
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(400, 300)
        
        # Load QSS styles
        self.load_styles()
        
        layout = QVBoxLayout()
        
        # Welcome label with title class
        label = QLabel('Welcome to Movie Ticket Booking System')
        label.setAlignment(Qt.AlignCenter)
        label.setProperty("class", "title")
        layout.addWidget(label)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Buttons with specific object names for styling
        self.user_btn = QPushButton('Book Ticket')
        self.user_btn.setObjectName("book_btn")
        
        self.cancel_btn = QPushButton('Cancel Booking')
        self.cancel_btn.setObjectName("cancel_btn")
        
        self.admin_btn = QPushButton('Admin Panel')
        self.admin_btn.setObjectName("admin_btn")
        
        # Add buttons with spacing
        layout.addWidget(self.user_btn)
        layout.addSpacing(10)
        layout.addWidget(self.cancel_btn)
        layout.addSpacing(10)
        layout.addWidget(self.admin_btn)
        
        # Add stretch to push buttons to center
        layout.addStretch()
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Connect buttons
        self.user_btn.clicked.connect(self.open_user_dialog)
        self.cancel_btn.clicked.connect(self.open_cancel_dialog)
        self.admin_btn.clicked.connect(self.open_admin_dialog)

    def load_styles(self):
        """Load and apply QSS styles from external file"""
        try:
            style_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.qss')
            with open(style_file, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Style file not found at {style_file}")
        except Exception as e:
            print(f"Error loading styles: {e}")

    def open_user_dialog(self):
        dialog = UserBookingDialog()
        dialog.exec_()

    def open_cancel_dialog(self):
        dialog = UserCancelDialog()
        dialog.exec_()

    def open_admin_dialog(self):
        dialog = AdminLoginDialog()
        dialog.exec_()

# For standalone testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 