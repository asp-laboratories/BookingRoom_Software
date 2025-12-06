import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.DatosClienteService import DatosClienteService
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices
from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "registro_cliente.ui"


cliente = DatosClienteService()
telefono = TelefonoServices()

class RegistroCliente():
    def __init__(self):
        self.registro_cliente = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.registro_cliente.show()
        self.registro_cliente.clienteConfirmar.clicked.connect(self.registrar_cliente)
        self.deshabilitar_telefonos()
        self.registro_cliente.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.registro_cliente.cbTelefono3.toggled.connect(self.ingresar_tercerTel)
        
        self.registro_cliente.cbTipoFisica.toggled.connect(self.seleccionar_fisica)
        self.registro_cliente.cbTipoMoral.toggled.connect(self.seleccionar_moral)
        self.registro_cliente.reNombreFiscal.setEnabled(False)
        
    def registrar_cliente(self):
        tipo_cliente = ""
        if self.registro_cliente.cbTipoFisica.isChecked():
            tipo_cliente = "TCLPF"

        if self.registro_cliente.cbTipoMoral.isChecked():
            tipo_cliente= "TCLPM"

        rfc = self.registro_cliente.reRfc.text()
        if (not permitir_ingreso(rfc, 'rfc')) or len(rfc) < 2:
            self.registro_cliente.reRfc.selectAll()
            self.registro_cliente.reRfc.setFocus()
            return

        nombre = self.registro_cliente.reNombre.text()
        if (not permitir_ingreso(nombre, 'onlytext')) or len(nombre) < 2:
            self.registro_cliente.reNombre.selectAll()
            self.registro_cliente.reNombre.setFocus()
            return

        priApellido = self.registro_cliente.reApellPat.text()
        if (not permitir_ingreso(nombre, 'onlytext')) or len(priApellido) < 2:
            self.registro_cliente.reApellPat.selectAll()
            self.registro_cliente.reApellPat.setFocus()
            return

        priAmater = self.registro_cliente.reApellMa.text()
        if (not permitir_ingreso(nombre, 'onlytext')) or len(priApellido) < 2:
            self.registro_cliente.reApellMa.selectAll()
            self.registro_cliente.reApellMa.setFocus()
            return

        resultado = cliente.registrar_clientes(rfc, nombre, priApellido, self.registro_cliente.reApellMa.text(), self.registro_cliente.reNombreFiscal.text(), self.registro_cliente.reCorreo.text(), self.registro_cliente.reColonia.text(), self.registro_cliente.reCalle.text(), int(self.registro_cliente.reNumero.text()), tipo_cliente)

        telefono.registrar_telefono(self.registro_cliente.reTelefono1.text(), self.registro_cliente.reRfc.text(),None)
        telefono.registrar_telefono(self.registro_cliente.reTelefono2.text(), self.registro_cliente.reRfc.text(),None)
        telefono.registrar_telefono(self.registro_cliente.reTelefono3.text(), self.registro_cliente.reRfc.text(),None)
        
        if resultado == None:
            QMessageBox.information(self.registro_cliente, "Error al crear cliente",  f"No se pudo registrar el cliente:")
        else:
            QMessageBox.information(self.registro_cliente, "Cliente registrado",  f"Cliente registrado: {nombre} {priApellido} {priAmater}")
    
    def deshabilitar_telefonos(self):
        self.registro_cliente.reTelefono2.setEnabled(False)
        self.registro_cliente.reTelefono3.setEnabled(False)
    
    def ingresar_segundoTel(self, estado):
        self.registro_cliente.reTelefono2.setEnabled(estado)
        
    def ingresar_tercerTel(self, estado):
        self.registro_cliente.reTelefono3.setEnabled(estado)

    def seleccionar_fisica(self, estado):
        if estado:
            self.registro_cliente.cbTipoMoral.setChecked(False)
            self.registro_cliente.reNombreFiscal.setEnabled(False)
            nombre_fiscal = f"{self.registro_cliente.reNombre.text()} {self.registro_cliente.reApellPat.text()} {self.registro_cliente.reApellMa.text()}"
            self.registro_cliente.reNombreFiscal.setText(nombre_fiscal)
            self.registro_cliente.clNombre.setText("Nombre")
            self.registro_cliente.clAp.setText("Apellido paterno")
            self.registro_cliente.clAm.setText("Apellido materno")

    def seleccionar_moral(self, estado):
        if estado:
            self.registro_cliente.cbTipoFisica.setChecked(False)
            self.registro_cliente.reNombreFiscal.setEnabled(True)
            self.registro_cliente.clNombre.setText("Nombre del contacto")
            self.registro_cliente.clAp.setText("Apellido paterno del contacto")
            self.registro_cliente.clAm.setText("Apellido materno del contacto")
 

    # def initGUI(self):
    #     self.registro_cliente.btnRegistrar.clicked.connect(self.registrar)
