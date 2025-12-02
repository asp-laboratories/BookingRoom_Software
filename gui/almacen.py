import os
from pathlib import Path
from datetime import datetime, date, timedelta
from PyQt6 import uic
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt6.QtCore import QDate, Qt
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService

from services.mobiliarioService import mobiliarioService
from utils.Formato import permitir_ingreso
ruta_ui = Path(__file__).parent / "almacen.ui"

equipamiento = EquipamentoService()
mobiliario = mobiliarioService()  




class Almacenista():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)
        
        #Mensaje para evaluar las operaciones

        #Ocultamiento de los submenus de los tres apartados
        self.navegacion.subMenuAlmacen.setVisible(False)
   
        # self.navegacion.widget.layout()
        #Abrir las subopciones
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
 
        self.navegacion.mobiliario_2.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.mobiliario.clicked.connect(lambda: self.mostrar_pagina(7))

        self.navegacion.almConfirmar.clicked.connect(self.actualizar_estado_mob)
        self.navegacion.almConfirmar_2.clicked.connect(self.actualizar_estado_equipa)
        self.navegacion.almBuscarM.clicked.connect(self.buscar_estado_mobiliario)
        self.navegacion.almBuscarE.clicked.connect(self.buscar_estado_equipamiento)

        #Variables utilizadas para almacenar informatcion

    def actualizar_estado_mob(self):
        resultado = mobiliario.actu_esta_mob(int(self.navegacion.almNum.text()),int(self.navegacion.almCantidad.text()),self.navegacion.almEstadoAntiguo.text(), self.navegacion.almNuevoEstado.text())
        if resultado == False:
            self.navegacion.almMensaje.setText("Incorrecto")
        else:
            self.navegacion.almMensaje.setText("Correcto")

    def actualizar_estado_equipa(self):
        resultado = equipamiento.actualizar_estado_equipamiento(int(self.navegacion.numE.text()),self.navegacion.almEstadoE.text(), self.navegacion.almEstadoO.text(),int(self.navegacion.almCantidade.text()))
        if resultado == False:
            self.navegacion.almMensaje_2.setText("Incorrecto")
        else:
            self.navegacion.almMensaje_2.setText("Correcto")
            
    def buscar_estado_mobiliario(self):
        resultado = mobiliario.obtener_mob_estado(self.navegacion.almBuscadorM.text())
        if resultado == None:
            pass
        else:
            mensaje = "\n---MOBILIARIOS---\n"
            for mob in resultado:
                mensaje += f"\nMobiliario: {mob["Numero"]}.\nNombre: {mob["Nombre"]}.\nEstado Actual: {mob["Estado"]}\nCantidad: {mob["Cantidad"]}\n"
                self.navegacion.almResultadoM.setText(mensaje)
    
    
    def buscar_estado_equipamiento(self):
        self.navegacion.almResulE.clear()
        resultado = equipamiento.obtener_equipa_estado(self.navegacion.almBuscadorE.text())
        if resultado == None:
            pass
        else:
            mensaje = "\n---EQUIPAMIENTOS---\n"
            for equi in resultado:
                mensaje += f"\nEquipamiento: {equi["Numero"]}.\nNombre: {equi["Nombre"]}.\nEstado Actual: {equi["Estado"]}\nCantidad: {equi["Cantidad"]}\n"
                self.navegacion.almResulE.setText(mensaje)


    def volver_login(self, link):
        from gui.login import Login
        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
