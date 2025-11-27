import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TrabajadorServices import TrabajadorServices
ruta_ui = Path(__file__).parent / "admin_screen.ui"
servicio = ServicioService()
salon = SalonServices()  
equipamiento = EquipamentoService()
trabajador = TrabajadorServices()


class AdministradorScreen():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.sMensaje.setText("")
        self.navegacion.saMensaje.setText("")
        self.navegacion.eMensaje.setText("")
        # self.navegacion.atMensaR.setText("")
        # self.navegacion.atMenaje.setText("")



        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)
        # self.navegacion.widget.layout()
        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)


        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))
        self.navegacion.salon.clicked.connect(lambda: self.mostrar_pagina(3))
        # self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))

        self.navegacion.sConfirmar.clicked.connect(self.registar_servicio) 
        self.navegacion.sConfirmarAct.clicked.connect(self.actualizar_servicio)
        

        self.navegacion.eConfirmar.clicked.connect(self.registrar_equipamiento)

        self.navegacion.saConfirmar.clicked.connect(self.registrar_salon)
        self.navegacion.saCancelar.clicked.connect(self.limpiar_salon)
        
        self.navegacion.atConfirmar.clicked.connect(self.establecer_rol)
        self.navegacion.atBuscar.clicked.connect(self.buscar)
        

        # self.cargar_seleccion_salon()
        # self.navegacion.reSalonInfo.clicked.connect(self.mostrar_info_salon)


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

    def actualizar_servicio(self):
        resultado = servicio.actualizar_campos(self.navegacion.sCampo.text(), int(self.navegacion.sNumeroServicio.text()) , self.navegacion.sNuevoValor.text())
        if resultado == False:
            self.navegacion.sMensajeAct.setText("Incorrecto")
        else:
            self.navegacion.sMensajeAct.setText("Correcto")



            
    def registrar_salon(self):
        largo =  float(self.navegacion.saLargo.text()) 
        ancho = float(self.navegacion.saAncho.text())
        altura =  float(self.navegacion.saAltura.text())
        m2 = (2*(largo+ancho)*altura)
        self.navegacion.saResultadoM2.setText(str(m2))
        resultado = salon.registrar_salones(self.navegacion.saNombre.text(), float(self.navegacion.saCostoRenta.text()), self.navegacion.saNombrePasillo.text(), self.navegacion.saNumeroPasillo.text(), largo, ancho, altura, m2)
        if resultado == False:
            self.navegacion.saMensaje.setText("Incorrecto")
        else:
            self.navegacion.saMensaje.setText("Correcto")
    
    def registrar_equipamiento(self):
        resultado = equipamiento.registrar_equipamento(self.navegacion.eNombreEqui.text(),self.navegacion.eDescripcion.text(), float(self.navegacion.eCostoRenta.text()), int(self.navegacion.eStock.text()), self.navegacion.eTipoEquipamiento.text())
        if resultado == False:
            self.navegacion.eMensaje.setText("Incorrecto")
        else:
            self.navegacion.eMensaje.setText("Correcto")




    def limpiar_salon(self):
        self.navegacion.saNombre.clear()
        self.navegacion.saCostoRenta.clear()
        self.navegacion.saNombrePasillo.clear()
        self.navegacion.saNumeroPasillo.    clear()
        self.navegacion.saLargo.clear()
        self.navegacion.saAncho.clear()
        self.navegacion.saAltura.clear()
        self.navegacion.saResultadoM2.clear()

    def buscar(self):
        resultado = trabajador.buscar_al_trabajador(self.navegacion.atBuscador.text())
        if resultado == None:
            self.navegacion.atMensaje.setText("Incorrecto")
        else:
            mensaje = "\n---TRABAJADORES---\n"
            for traba in resultado:
                mensaje += f"\nRFC: {traba["RFC"]}.\nNombre completo: {traba["nombre"]}.\nRol: {traba["rol"]}\n"
                self.navegacion.atResultadoText.setText(mensaje)
            self.navegacion.atMensaje.setText("Correcto")
         
        
    def establecer_rol(self):
        resultado = trabajador.actualizar_roles(self.navegacion.atRfc.text(), self.navegacion.atNombreR.text())
        if resultado == None:
            self.navegacion.atMensaR.setText("Correcto")
        else:
            self.navegacion.atMensaR.setText("Incorrecto")



    def mostrar_pagina(self, indice):
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    
    # def cargar_seleccion_salon(self):
    #     self.navegacion.reSalonSelecc.clear()
    #     self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
    #     obtener = salon.listar_salones()
    #     for sln in obtener:
    #         self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])
    
    # def mostrar_info_salon(self):
    #     salNumero = self.navegacion.reSalonSelecc.currentData()
    #     sali = self.buscar_usuario_por_id(salNumero)
    #     mensaje = "INFORMACION DEL SALON"
    #     mensaje += f"\n NOMBRE: {sali["nombre"]}"
    #     mensaje += f"\n COSTO: {str(sali["costoRenta"])}"
    #     if sali:
    #         self.navegacion.resultadoSalon.setText(mensaje)
    
    # def buscar_usuario_por_id(self, salNumero):
    #     for s in salon.listar_salones():
    #         if s["numSalon"] == salNumero:
    #             return s
    #     return None




    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
