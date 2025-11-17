import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
ruta_ui = Path(__file__).parent / "admin.ui"

class AdminWindow():
    def __init__(self):
        self.admin = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.admin.showMaximized()


