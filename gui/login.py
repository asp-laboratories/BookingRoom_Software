import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from gui.admin import AdminWindow
from gui.admin_screen import AdministradorScreen
from gui.deftl import DefaultWindow
from gui.navegacion import Navegacion
from gui.registro import Registro
from services.LoginService import LoginService

ruta_ui = Path(__file__).parent / "login.ui"
log = LoginService()

class Login():
    def __init__(self):
        self.login = uic.loadUi(str(ruta_ui))
        self.initGUI()
        self.login.mensaje.setText("")
        self.login.labelLink.linkActivated.connect(self.abrir_registro)
        self.login.show()

    def abrir_registro(self, link):
        if link == "registro":
            self.login.hide()  # Ocultar ventana actual
            self.ventana_registro = Registro()
            

    def ingresar(self):
        if len(self.login.leEmail.text()) < 2:
            self.login.mensaje.setText("Ingrese un email valido")
            self.login.leEmail.setFocus()
        elif len(self.login.leNumero.text()) < 2:
            self.login.mensaje.setText("Ingrese un numero de trabajador valido")
            self.login.leNumero.setFocus()
        else:
            self.login.mensaje.setText("")
            resultado = log.registrar_trabajadores(self.login.leEmail.text(), self.login.leNumero.text())
            if resultado == None:
                self.login.mensaje.setText("Incorrecto")
            else:
                self.login.mensaje.setText("Correcto")
                if resultado[2] == "DEFLT":
                    self.nav = Navegacion()
                    self.login.hide()
                elif resultado[2] == "ADMIN":

                    self.admin = AdministradorScreen()
                    # self.admin = AdminWindow()
                    self.login.hide()

    def initGUI(self):
        self.login.btnIniciar.clicked.connect(self.ingresar)



# Método 1: Con pathlib (recomendado)
# self.login = uic.loadUi(str(ruta_ui))

# Método 2: Con os.path
# ruta_actual = os.path.dirname(__file__)
# ruta_ui = os.path.join(ruta_actual, "login-ui.ui")
# self.login = uic.loadUi(ruta_ui)
