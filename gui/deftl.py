import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
ruta_ui = Path(__file__).parent / "deftl.ui"

class DefaultWindow():
    def __init__(self):
        self.deftl = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.deftl.showMaximized()


