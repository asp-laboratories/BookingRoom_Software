import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices
from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "registro_cliente.ui"

class RegistroCliente():
    def __init__(self):
        self.registro_cliente = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.registro_cliente.show()


 

    # def initGUI(self):
    #     self.registro_cliente.btnRegistrar.clicked.connect(self.registrar)
