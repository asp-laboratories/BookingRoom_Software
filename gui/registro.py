import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices

ruta_ui = Path(__file__).parent / "registro.ui"
trabajador = TrabajadorServices()
telefono = TelefonoServices()
class Registro():
    def __init__(self):
        self.registro = uic.loadUi(str(ruta_ui))
        self.initGUI()
        self.registro.mensaje.setText("")
        self.registro.labelLink.linkActivated.connect(self.volver_login)
        self.deshabilitar_telefonos()
        self.registro.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.registro.cbTelefono3.toggled.connect(self.ingresar_tercerTel)
        self.registro.show()

    
    def volver_login(self, link):
        from gui.login import Login
        if link == "iniciar":
            self.registro.hide()
            self.login = Login()
 
    def registrar(self):
        if len(self.registro.leRfc.text()) < 2:
            self.registro.mensaje.setText("Ingrese un RFC valido")
            self.registro.leEmail.setFocus()
        elif len(self.registro.leNumero.text()) < 2:
            self.registro.mensaje.setText("Ingrese un numero de trabajador valido")
            self.registro.leNumero.setFocus()

        elif len(self.registro.leNombre.text()) < 2:
            self.registro.mensaje.setText("Ingrese un nombre valido")
            self.registro.leNombre.setFocus()

        elif len(self.registro.leApaterno.text()) < 2:
            self.registro.mensaje.setText("Ingrese un apellido paterno valido")
            self.registro.leApaterno.setFocus()

        elif len(self.registro.leAmaterno.text()) < 2:
            self.registro.mensaje.setText("Ingrese un apellido materno valido")
            self.registro.leAmaterno.setFocus()

        elif len(self.registro.leEmail.text()) < 2:
            self.registro.mensaje.setText("Ingrese un email valido")
            self.registro.leEmail.setFocus()

        else:
            self.registro.mensaje.setText("")
            resultado = trabajador.registrar_trabajadores(self.registro.leRfc.text(), self.registro.leNumero.text(), self.registro.leNombre.text(), self.registro.leApaterno.text(),self.registro.leAmaterno.text(), self.registro.leEmail.text())
            
            telefono.registrar_telefono(self.registro.leTelefono.text(), None,self.registro.leRfc.text())
            telefono.registrar_telefono(self.registro.leTelefono2.text(), None,self.registro.leRfc.text())
            telefono.registrar_telefono(self.registro.leTelefono3.text(), None,self.registro.leRfc.text())
            if resultado == False:
                self.registro.mensaje.setText("Incorrecto")
            else:
                self.registro.mensaje.setText("Correcto")
    def deshabilitar_telefonos(self):
        self.registro.leTelefono2.setEnabled(False)
        self.registro.leTelefono3.setEnabled(False)
    def ingresar_segundoTel(self, estado):
        self.registro.leTelefono2.setEnabled(estado)
    
    def ingresar_tercerTel(self, estado):
        self.registro.leTelefono3.setEnabled(estado)


    def initGUI(self):
        self.registro.btnRegistrar.clicked.connect(self.registrar)
