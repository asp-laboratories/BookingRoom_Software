import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices
from utils.Formato import permitir_ingreso

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

        rfc = self.registro.leRfc.text()
        if (len(rfc) < 2) or (not permitir_ingreso(rfc, 'rfc')):
            self.registro.mensaje.setText("Ingrese un RFC valido")
            self.registro.leRfc.selectAll()
            self.registro.leRfc.setFocus()
            return

        numTrabajador = self.registro.leNumero.text()
        if (len(numTrabajador) < 2) or (not permitir_ingreso(numTrabajador, 'numtraba')):
            self.registro.mensaje.setText("Ingrese un numero de trabajador valido")
            self.registro.leNumero.selectAll()
            self.registro.leNumero.setFocus()
            return

        nombre = self.registro.leNombre.text()
        if (len(nombre) < 2) or (not permitir_ingreso(nombre, 'onlytext')):
            self.registro.mensaje.setText("Ingrese un nombre valido")
            self.registro.leNombre.selectAll()
            self.registro.leNombre.setFocus()
            return

        apePater = self.registro.leApaterno.text()
        if (len(apePater) < 2) or (not permitir_ingreso(apePater, 'onlytext')):
            self.registro.mensaje.setText("Ingrese un apellido paterno valido")
            self.registro.leApaterno.selectAll()
            self.registro.leApaterno.setFocus()
            return

        apeMater = self.registro.leAmaterno.text()
        if not (apeMater == ""):
            if (len(apeMater) < 2) or (not permitir_ingreso(apeMater, 'onlytext')):
                self.registro.mensaje.setText("Ingrese un apellido materno valido")
                self.registro.leAmaterno.selectAll()
                self.registro.leAmaterno.setFocus()
                return
        else:
            apeMater = None

        email = self.registro.leEmail.text()
        if (len(email) < 2) or (not permitir_ingreso(email, 'correo')):
            self.registro.mensaje.setText("Ingrese un correo valido")
            self.registro.leEmail.selectAll()
            self.registro.leEmail.setFocus()
            return

        resultado = trabajador.registrar_trabajadores(rfc, numTrabajador, nombre, apePater, apeMater, email)

        if not resultado:
            self.registro.mensaje.setText("Error al registrar trabajador")
        else:
            self.registro.mensaje.setText("Trabajador registrado")            
            telefono.registrar_telefono(self.registro.leTelefono.text(), None, rfc)
            telefono.registrar_telefono(self.registro.leTelefono2.text(), None, rfc)
            telefono.registrar_telefono(self.registro.leTelefono3.text(), None, rfc)
    
    
    def deshabilitar_telefonos(self):
        self.registro.leTelefono2.setEnabled(False)
        self.registro.leTelefono3.setEnabled(False)
    def ingresar_segundoTel(self, estado):
        self.registro.leTelefono2.setEnabled(estado)
    
    def ingresar_tercerTel(self, estado):
        self.registro.leTelefono3.setEnabled(estado)


    def initGUI(self):
        self.registro.btnRegistrar.clicked.connect(self.registrar)
