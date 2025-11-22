import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox


ruta_ui = Path(__file__).parent / "navegacion.ui"

class Navegacion():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()

        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)

        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)

        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(not self.navegacion.subMenuAdministracion.isVisible())
    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(not self.navegacion.subMenuAlmacen.isVisible())
    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(not self.navegacion.subMenuRecepcion.isVisible())

    def mostrar_pagina(self, indice):
        self.navegacion.stackedWidget.setCurrentIndex(indice)



    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
