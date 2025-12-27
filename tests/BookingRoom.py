import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt6.QtWidgets import QApplication
from gui.login import Login


class BookingRoom:
    def __init__(self) -> None:
        self.app = QApplication([])
        self.login = Login()
        self.app.exec()
