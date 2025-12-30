from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
import os

class HorarioView(QWidget):
    def __init__(self):
        super().__init__()
        # Construir la ruta al archivo .ui
        ui_path = os.path.join(os.path.dirname(__file__), 'horario_view.ui')
        uic.loadUi(ui_path, self)
