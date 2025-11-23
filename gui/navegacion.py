import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from services.ServicioServices import ServicioService
ruta_ui = Path(__file__).parent / "navegacion.ui"
servicio = ServicioService()

class Navegacion():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.sMensaje.setText("")
        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)

        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)

        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))

        self.navegacion.sConfirmar.clicked.connect(self.registar_servicio)

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(not self.navegacion.subMenuAdministracion.isVisible())
    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(not self.navegacion.subMenuAlmacen.isVisible())
    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(not self.navegacion.subMenuRecepcion.isVisible())

    def registar_servicio(self):
        resultado = servicio.registrar_servicio(self.navegacion.sNombreSer.text(), self.navegacion.sDescripcion.text(), self.navegacion.sCostoRenta.text(), self.navegacion.sTipoServicio.text())
        if resultado == False:
            self.navegacion.sMensaje.setText("Incorrecto")
        else:
            self.navegacion.sMensaje.setText("Correcto")

    def mostrar_pagina(self, indice):
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    



    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
