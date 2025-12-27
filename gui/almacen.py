from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from services.EquipamentoService import EquipamentoService

from services.mobiliarioService import mobiliarioService

ruta_ui = Path(__file__).parent / "almacen.ui"

equipamiento = EquipamentoService()
mobiliario = mobiliarioService()


class Almacenista:
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)

        # Mensaje para evaluar las operaciones

        # Ocultamiento de los submenus de los tres apartados
        self.navegacion.subMenuAlmacen.setVisible(False)

        # self.navegacion.widget.layout()
        # Abrir las subopciones
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)

        self.navegacion.mobiliario.clicked.connect(lambda: self.mostrar_pagina(7))

        self.navegacion.almConfirmar.clicked.connect(self.actualizar_estado_mob)
        self.navegacion.almConfirmar_2.clicked.connect(self.actualizar_estado_equipa)
        self.navegacion.almBuscarM.clicked.connect(self.buscar_estado_mobiliario)
        self.navegacion.almBuscarE.clicked.connect(self.buscar_estado_equipamiento)

    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(
            not self.navegacion.subMenuAlmacen.isVisible()
        )
        # Variables utilizadas para almacenar informatcion

    def actualizar_estado_mob(self):
        resultado = mobiliario.actu_esta_mob(
            int(self.navegacion.almNum.text()),
            int(self.navegacion.almCantidad.text()),
            self.navegacion.almEstadoAntiguo.text(),
            self.navegacion.almNuevoEstado.text(),
        )
        if not resultado:
            QMessageBox.warning(self.navegacion, "Error de actualización", "La actualización del estado del mobiliario fue incorrecta.")
        else:
            QMessageBox.information(self.navegacion, "Actualización exitosa", "El estado del mobiliario se actualizó correctamente.")

    def actualizar_estado_equipa(self):
        resultado = equipamiento.actualizar_estado_equipamiento(
            int(self.navegacion.numE.text()),
            self.navegacion.almEstadoE.text(),
            self.navegacion.almEstadoO.text(),
            int(self.navegacion.almCantidade.text()),
        )
        if not resultado:
            QMessageBox.warning(self.navegacion, "Error de actualización", "La actualización del estado del equipamiento fue incorrecta.")
        else:
            QMessageBox.information(self.navegacion, "Actualización exitosa", "El estado del equipamiento se actualizó correctamente.")

    def buscar_estado_mobiliario(self):
        resultado = mobiliario.obtener_mob_estado(self.navegacion.almBuscadorM.text())
        if resultado is None:
            pass
        else:
            mensaje = "\n---MOBILIARIOS---\n"
            for mob in resultado:
                mensaje += f"\nMobiliario: {mob['Numero']}.\nNombre: {mob['Nombre']}.\nEstado Actual: {mob['Estado']}\nCantidad: {mob['Cantidad']}\n"
                self.navegacion.almResultadoM.setText(mensaje)

    def buscar_estado_equipamiento(self):
        self.navegacion.almResulE.clear()
        resultado = equipamiento.obtener_equipa_estado(
            self.navegacion.almBuscadorE.text()
        )
        if resultado is None:
            pass
        else:
            mensaje = "\n---EQUIPAMIENTOS---\n"
            for equi in resultado:
                mensaje += f"\nEquipamiento: {equi['Numero']}.\nNombre: {equi['Nombre']}.\nEstado Actual: {equi['Estado']}\nCantidad: {equi['Cantidad']}\n"
                self.navegacion.almResulE.setText(mensaje)

    def mostrar_pagina(self, indice):
        self.navegacion.scrollAreaContenido.verticalScrollBar().setValue(0)
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    def volver_login(self, link):
        from gui.login import Login

        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
