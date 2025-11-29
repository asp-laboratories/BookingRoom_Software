import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit, QMessageBox, QListWidgetItem, QVBoxLayout
from PyQt6.QtCore import Qt
from models.MobCarac import MobCarac
from services.DatosClienteService import DatosClienteServices
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices
from services.mobiliarioService import mobiliarioService
ruta_ui = Path(__file__).parent / "admin_screen.ui"

servicio = ServicioService()
salon = SalonServices()  
equipamiento = EquipamentoService()
trabajador = TrabajadorServices()
cliente = DatosClienteServices()
telefono = TelefonoServices()
mobiliario = mobiliarioService()  

class AdministradorScreen():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)
        self.navegacion.sMensaje.setText("")
        self.navegacion.saMensaje.setText("")
        self.navegacion.eMensaje.setText("")
        self.navegacion.atMensaR.setText("")
        self.navegacion.atMensaje.setText("")
        self.navegacion.mobMensaje.setText("")


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
        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(6))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))

        self.navegacion.sConfirmar.clicked.connect(self.registar_servicio) 
        self.navegacion.sConfirmarAct.clicked.connect(self.actualizar_servicio)
        self.navegacion.slBuscar.clicked.connect(self.listar_servicio) 
        self.navegacion.seConfirmar.clicked.connect(self.eliminar_servicio)
        self.navegacion.eConfirmar.clicked.connect(self.registrar_equipamiento)

        self.navegacion.saConfirmar.clicked.connect(self.registrar_salon)
        self.navegacion.saCancelar.clicked.connect(self.limpiar_salon)

        self.navegacion.amConfirmar.clicked.connect(self.generar_caracteristicas)
        self.navegacion.amConfirmar_2.clicked.connect(self.registrar_mobiliario)
        # self.navegacion.amConfirmar_2.clicked.connect(self.obtener_valores_inputs)
        
        self.navegacion.atConfirmar.clicked.connect(self.establecer_rol)
        self.navegacion.atBuscar.clicked.connect(self.buscar)
        
        self.navegacion.clienteConfirmar.clicked.connect(self.registrar_cliente)
        self.deshabilitar_telefonos()
        self.navegacion.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.navegacion.cbTelefono3.toggled.connect(self.ingresar_tercerTel)
        self.navegacion.cbTipoFisica.toggled.connect(self.seleccionar_fisica)
        self.navegacion.cbTipoMoral.toggled.connect(self.seleccionar_moral)

        self.cargar_seleccion_salon()
        self.navegacion.reSalonInfo.clicked.connect(self.mostrar_info_salon)
        self.cargar_listas()
        self.inputs = []
        self.inputs_tipo = []

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

    def listar_servicio(self):
        self.navegacion.sResultadoListar.clear()
        resultado = servicio.listar_servicio_busqueda(self.navegacion.slIngresarBusqueda.text())
        if resultado == False:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for ser in resultado:
                mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
                self.navegacion.sResultadoListar.setText(mensaje)
           
    def eliminar_servicio(self):
        resultado = servicio.eliminar_fila(int(self.navegacion.seEliminarInput.text()))
        if resultado == False:
            pass
        else:
            self.navegacion.seMensajeE.setText("Correcto")





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

    #
    # def registrar_mobiliario(self):
    #     nombre = self.navegacion.mobNombre.text()
    #     costoRenta = float(self.navegacion.mobCostoRenta.text())
    #     stock = int(self.navegacion.mobStock.text())
    #     tipo = self.navegacion.mobTipo.text()
    #     print(nombre)
    #     print(costoRenta)
    #
    #     print(stock)
    #     print(tipo)
    #     valor = []        
    #     for i, caracteristica in enumerate(self.inputs):
    #         valor.append(caracteristica.text())
    #
    #     valor_tipo = []
    #     for i, tipo in enumerate(self.inputs_tipo):
    #         valor_tipo.append(tipo.text())
    #     
    #     caracteristicas = []
    #     print(valor[0])
    #     print(valor_tipo[0])
    #     caracteristica = MobCarac(valor[0], valor_tipo[0])
    #     print(caracteristica)
    #     caracteristicas.append(caracteristica)
    #     
    #     resultado = mobiliario.registrar_mobiliario(nombre, costoRenta, stock, tipo, caracteristicas)
    #     if resultado == False:
    #         self.navegacion.mobMensaje.setText("Incorrecto")
    #     else:
    #         self.navegacion.mobMensaje.setText("Correcto")

    def registrar_mobiliario(self):
        # 1. Obtención de datos principales (SIN CAMBIOS)
        try:
            nombre = self.navegacion.mobNombre.text()
            costoRenta = float(self.navegacion.mobCostoRenta.text())
            stock = int(self.navegacion.mobStock.text())
            tipo = self.navegacion.mobTipo.text()
        except ValueError:
            self.navegacion.mobMensaje.setText("Error: Costo o Stock deben ser números válidos.")
            return

        print(nombre)
        print(costoRenta)
        print(stock)
        print(tipo)

        # 2. Recolección de textos de los inputs (SIN CAMBIOS)
        valor = []         
        for caracteristica_input in self.inputs:
            valor.append(caracteristica_input.text())

        valor_tipo = []
        for tipo_input in self.inputs_tipo:
            valor_tipo.append(tipo_input.text())
        
        # 3. CORRECCIÓN: Iterar para crear TODOS los objetos MobCarac
        caracteristicas = []
        # El número de características es la longitud de cualquiera de las listas (deben ser iguales)
        num_caracteristicas = len(valor) 

        for i in range(num_caracteristicas):
            nombre_carac = valor[i]
            tipo_carac = valor_tipo[i]

            # Verificación simple para evitar crear características vacías
            if nombre_carac.strip() and tipo_carac.strip():
                caracteristica = MobCarac(nombre_carac, tipo_carac)
                print(f"Característica creada: {caracteristica}")
                caracteristicas.append(caracteristica)
            else:
                 print(f"Omitiendo característica {i+1} porque está vacía.")
            
        # 4. Llamada a la función de registro (SIN CAMBIOS, AHORA CON LA LISTA COMPLETA)
        resultado = mobiliario.registrar_mobiliario(nombre, costoRenta, stock, tipo, caracteristicas)
        
        if resultado == False:
            self.navegacion.mobMensaje.setText("Incorrecto")
        else:
            self.navegacion.mobMensaje.setText("Correcto")
    def limpiar_caracteristicas(self):
        lay = self.navegacion.mobcont2.layout()

        while lay.count():
            child = lay.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.inputs.clear()

    
    def generar_caracteristicas(self):
        lay = self.navegacion.mobcont2.layout()
        cantidad = self.navegacion.seleccionCaracteristicas.value()
        for i in range(cantidad):
            input_caracteristica = QLineEdit()
            input_caracteristica.setPlaceholderText(f"Ingrese el nombre de la caracteristica {i+1}:")
            # input_caracteristica.setObjectName(f"input_caracteristica_{i}")
            input_caracteristica.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ecf0f1;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #3498db;
            }
            """)

            input_tipo_carac = QLineEdit()
            input_tipo_carac.setPlaceholderText(f"Ingrese el tipo de caracteristica {i+1}: ")
            input_tipo_carac.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: #ecf0f1;
                color: #000000;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #3498db;
            }
            """)
            lay.addWidget(input_caracteristica)
            lay.addWidget(input_tipo_carac)
            self.inputs.append(input_caracteristica)
            self.inputs_tipo.append(input_tipo_carac)
        
        # valor = []        
        # for i, caracteristica in enumerate(self.inputs):
        #     valor.append(caracteristica.text())
        #
        # valor_tipo = []
        # for i, tipo in enumerate(self.inputs_tipo):
        #     valor_tipo.append(tipo.text())


            print("Yes")

    # def valores(self):
    #     valor = []
    #     for i, caracteristica in enumerate(self.inputs):
    #         valor.append(caracteristica.text())
    #         # valor.append(f"Input {i +1}: {val}")
    #         # for v in valor:
    #         #     print(v)
    #     return valor
    #
    # def valores_input(self):
    #     valor_tipo = []
    #     for i, tipo in enumerate(self.inputs_tipo):
    #         valor_tipo.append(tipo.text())
    #     return valor_tipo

    
    def mostrar_pagina(self, indice):
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    
    def registrar_cliente(self):
        resultado = cliente.registrar_clientes(self.navegacion.reRfc.text(), self.navegacion.reNombre.text(), self.navegacion.reApellPat.text(), self.navegacion.reApellMa.text(), self.navegacion.reNombreFiscal.text(), self.navegacion.reCorreo.text(), self.navegacion.reColonia.text(), self.navegacion.reCalle.text(), int(self.navegacion.reNumero.text()), "TCLPF")

        telefono.registrar_telefono(self.navegacion.reTelefono1.text(), self.navegacion.reRfc.text(),None)
        telefono.registrar_telefono(self.navegacion.reTelefono2.text(), self.navegacion.reRfc.text(),None)
        telefono.registrar_telefono(self.navegacion.reTelefono3.text(), self.navegacion.reRfc.text(),None)
        if resultado == False:
            self.navegacion.clienteMen.setText("Incorrecto")
        else:
            self.navegacion.clienteMen.setText("Corecto")

    def deshabilitar_telefonos(self):
        self.navegacion.reTelefono2.setEnabled(False)
        self.navegacion.reTelefono3.setEnabled(False)
    
    def ingresar_segundoTel(self, estado):
        self.navegacion.reTelefono2.setEnabled(estado)
    
    def ingresar_tercerTel(self, estado):
        self.navegacion.reTelefono3.setEnabled(estado)

    def seleccionar_fisica(self):
        self.navegacion.cbTipoMoral.setChecked(False)

    def seleccionar_moral(self):
        self.navegacion.cbTipoFisica.setChecked(False)


    def cargar_seleccion_salon(self):
        self.navegacion.reSalonSelecc.clear()
        self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
        obtener = salon.listar_salones()
        for sln in obtener:
            self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])
    
    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
        sali = self.buscar_usuario_por_id(salNumero)
        mensaje = "INFORMACION DEL SALON"
        mensaje += f"\n NOMBRE: {sali["nombre"]}"
        mensaje += f"\n COSTO: {str(sali["costoRenta"])}"
        if sali:
            self.navegacion.resultadoSalon.setText(mensaje)
    
    def buscar_usuario_por_id(self, salNumero):
        for s in salon.listar_salones():
            if s["numSalon"] == salNumero:
                return s
        return None


    def cargar_listas(self):
        self.navegacion.listaServicios.clear()
        self.navegacion.listaEquipamiento.clear()

        for servi in servicio.listar_servicio():
            texto = f"{servi['nombre']} - ${servi['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, servi)
            self.navegacion.listaServicios.addItem(item)

        for equipa in equipamiento.listar_equipamentos():
            texto = f"{equipa['nombre']} - ${equipa['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, equipa)
            self.navegacion.listaEquipamiento.addItem(item)
    
    def volver_login(self, link):
        from gui.login import Login
        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
