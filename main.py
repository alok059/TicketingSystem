# main.py
# Entry point for the Movie Ticket Booking System

from PyQt5.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 