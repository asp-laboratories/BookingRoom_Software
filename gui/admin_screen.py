import os
from pathlib import Path
from datetime import datetime, date, timedelta
from PyQt6 import uic
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt6.QtCore import QDate, Qt
from database_simulada import DatabaseSimulada
from models.MobCarac import MobCarac
from models.ReserEquipa import ReserEquipamiento
from services.DatosClienteService import DatosClienteService
from services.ReserEquipaService import ReserEquipaService
from services.ReservacionService import ReservacionService
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TelefonoServices import TelefonoServices
from services.TipoMontajeService import TipoMontajeService
from services.TipoServicioService import TipoServicioService
from services.TrabajadorServices import TrabajadorServices
from services.mobiliarioService import mobiliarioService
from utils.Formato import permitir_ingreso
ruta_ui = Path(__file__).parent / "admin_screen.ui"

tipo_servi = TipoServicioService()
db = DatabaseSimulada()
servicio = ServicioService()
salon = SalonServices()  
equipamiento = EquipamentoService()
trabajador = TrabajadorServices()
cliente = DatosClienteService()
telefono = TelefonoServices()
mobiliario = mobiliarioService()  
tipo_montaje = TipoMontajeService()
reservacion = ReservacionService()
reser_equipa = ReserEquipaService()



class AdministradorScreen():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)
        
        #Mensaje para evaluar las operaciones
        self.navegacion.sMensaje.setText("")
        self.navegacion.saMensaje.setText("")
        self.navegacion.eMensaje.setText("")
        self.navegacion.atMensaR.setText("")
        self.navegacion.atMensaje.setText("")
        self.navegacion.mobMensaje.setText("")

        #Ocultamiento de los submenus de los tres apartados
        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)
        # self.navegacion.widget.layout()

        #Abrir las subopciones
        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)


        #Navegacion entre paginas
        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))
        self.navegacion.salon.clicked.connect(lambda: self.mostrar_pagina(3))
        self.navegacion.mobiliario_2.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))
        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(6))
        self.navegacion.mobiliario.clicked.connect(lambda: self.mostrar_pagina(7))



        # Botones de los eventos de servicios
        self.navegacion.sConfirmar.clicked.connect(self.registar_servicio) 
        self.navegacion.sConfirmarAct.clicked.connect(self.actualizar_servicio)
        self.navegacion.slBuscar.clicked.connect(self.listar_servicio) 
        self.navegacion.slBuscar_3.clicked.connect(self.listar_servicio_act) 
        self.navegacion.slBuscar_2.clicked.connect(self.listar_servicio_del)

        self.navegacion.buscarTipo.clicked.connect(self.listar_servicio_segun_tipo)
        self.navegacion.tipoBuscarE.clicked.connect(self.buscar_tipoS_eli)    
        self.navegacion.seConfirmar.clicked.connect(self.eliminar_servicio)

        self.navegacion.buscarTipo_2.clicked.connect(self.listar_reservaciones)
        # Botones para los eventos de equipamiento
        self.navegacion.eConfirmar.clicked.connect(self.registrar_equipamiento)

        # Botones para los eventos de salones
        self.navegacion.saConfirmar.clicked.connect(self.registrar_salon)
        self.navegacion.saCancelar.clicked.connect(self.limpiar_salon)

        # Botones para los eventos de mobiliario
        self.navegacion.amConfirmar.clicked.connect(self.generar_caracteristicas)
        self.navegacion.amConfirmar_2.clicked.connect(self.registrar_mobiliario)
        # self.navegacion.amConfirmar_2.clicked.connect(self.obtener_valores_inputs)


        # Botones para los eventos de trabajadores
        self.navegacion.atConfirmar.clicked.connect(self.establecer_rol)
        self.navegacion.atBuscar.clicked.connect(self.buscar)
       
        self.navegacion.reConfirmar.clicked.connect(self.total_reservacion)
        
        #Botones para los eventos de actualizacion de roles por parte del almacenista
        self.navegacion.almConfirmar.clicked.connect(self.actualizar_estado_mob)
        self.navegacion.almBuscarM.clicked.connect(self.buscar_estado_mobiliario)
        self.navegacion.almBuscarE.clicked.connect(self.buscar_estado_equipamiento)

        
        # Eventos del cliente dentro de reservaciones
        self.navegacion.clienteConfirmar.clicked.connect(self.registrar_cliente)
        self.deshabilitar_telefonos()
        self.navegacion.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.navegacion.cbTelefono3.toggled.connect(self.ingresar_tercerTel)
        
        self.navegacion.cbTipoFisica.toggled.connect(self.seleccionar_fisica)
        self.navegacion.cbTipoMoral.toggled.connect(self.seleccionar_moral)
        
        
        self.cargar_seleccion_tipoMontaje()
        self.navegacion.reMontajeInfo.clicked.connect(self.mostrar_info_montaje)
        # Eventos de salones, equipamiento y servicios dentro de reservacion
        self.cargar_seleccion_salon()
        self.navegacion.reSalonInfo.clicked.connect(self.mostrar_info_salon)
        self.cargar_listas()
        self.cargar_lista_equipamiento()
        self.navegacion.listaEquipamiento.itemSelectionChanged.connect(self.mostrar_controles_cantidad)
        #self.navegacion.btnSubTotalE.clicked.connect(self.calcular_equipamiento)
         
        #Variables utilizadas para almacenar informatcion

        self.subtotal_servicios = 0.0
        self.subtotal_salon = 0.0 
        self.cantidades = {}
        self.controles_equipos = {}
        self.inputs = []
        self.inputs_tipo = []
        self.datos_finales = {} 
        self.fechas = []
        self.configurar_fechas_iniciales()
        
        
        # Controles del calendario
        self.navegacion.btnAgregar_2.clicked.connect(self.agregar_evento)
        self.navegacion.btnMostrar_2.clicked.connect(self.mostrar_eventos)
        self.navegacion.btnLimpiar_2.clicked.connect(self.limpiar_horario)
        self.navegacion.btnActualizar.clicked.connect(self.actualizar_fechas)

        self.navegacion.tableHorario.cellDoubleClicked.connect(self.celda_doble_clic)
        self.configurar_horario()

        # Metodos para abrir las subopciones

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(not self.navegacion.subMenuAdministracion.isVisible())
    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(not self.navegacion.subMenuAlmacen.isVisible())
    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(not self.navegacion.subMenuRecepcion.isVisible())

        # Seccion de servicios - logica de servicios

    def registar_servicio(self):
        nombre = self.navegacion.sNombreSer.text()
        if (len(nombre) < 2): # unica validacion?
            self.navegacion.sMensaje.setText("Ingresar un nombre valido")
            return
        
        descripcion = self.navegacion.sDescripcion.text()
        if (len(descripcion) < 2):
            self.navegacion.sMensaje.setText("Ingresar una descripcion valida")
            return

        resCostoRenta = self.navegacion.sCostoRenta.text()
        if not (permitir_ingreso(resCostoRenta, 'numfloat')):
            self.navegacion.sMensaje.setText("Ingrese un valor valido como costo de renta")
            return
        else:
            costo_renta = float(resCostoRenta)
        
        tipo_servicio = self.navegacion.sTipoServicio.text() # Combo box?
        if not (permitir_ingreso(tipo_servicio, 'onlytext')):
            self.navegacion.sMensaje.setText("Ingrese un tipo de servicio valido")
            return

        resultado = servicio.registrar_servicio(nombre, descripcion, costo_renta, tipo_servicio)

        if not resultado:
            self.navegacion.sMensaje.setText("Registro fallido")
        else:
            self.navegacion.sMensaje.setText("Registro concretado")

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
        
    def listar_servicio_act(self):
        self.navegacion.sResultadoListar_3.clear()
        resultado = servicio.listar_servicio_busqueda(self.navegacion.slIngresarBusqueda_3.text())
        if resultado == False:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for ser in resultado:
                mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
                self.navegacion.sResultadoListar_3.setText(mensaje)
        
    def listar_servicio_del(self):
        self.navegacion.sResultadoListar_2.clear()
        resultado = servicio.listar_servicio_busqueda(self.navegacion.slIngresarBusqueda_2.text())
        if resultado == False:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for ser in resultado:
                mensaje += f"\nNumero: {ser["numServicio"]}.\nNombre: {ser["nombre"]}.\nCosto Renta: {ser["costoRenta"]}\n"
                self.navegacion.sResultadoListar_2.setText(mensaje)

    def listar_servicios_del_mismo_tipo(self):
        self.navegacion.sResultadoListar_2.clear()
        resultado = servicio.servicios_tipo(self.navegacion.slIngresarBusqueda_2.text())
        if resultado == False:
            pass
        else:
            mensaje = "\n---SERVICIOS---\n"
            for st in resultado:
                mensaje += f"\nTipo de servicio: {st["tipo_servicio"]}"
                self.navegacion.sResultadoListar_2.setText(mensaje)




    def listar_reservaciones(self):
        self.navegacion.tResultadoS_2.clear()
        self.navegacion.tResultadoS_3.clear()
        resultado = reservacion.listar_reservacion_general(int(self.navegacion.tipoBuscar_2.text()))
        if resultado == False:
            pass
        else: 
            mensaje = "\n--RESERVACIONES---\n"
            for re in resultado:
                mensaje += f"\nReservacion: {re['num_reser']}\nFecha: {re["fecha_reser"]}\nCliente: {re["cliente"]}\nContacto: {re['cont_nombre']}\nCorreo electronico: {re['cliente_email']}\nFecha del evento: {re['fecha_even']}\nHora inicial: {re['hora_ini']} "
                self.navegacion.tResultadoS_2.setText(mensaje)

            resultadoE = reser_equipa.equipamiento_en_reser_listar(int(self.navegacion.tipoBuscar_2.text()))
            mensajeEQ = "\n---EQUIPAMIENTOS---\n"
            for ree in  resultadoE:
                mensajeEQ += f"\n Cliente {ree["cliente"]}"
                self.navegacion.tResultadoS_3.setText(mensajeEQ)





    def eliminar_servicio(self):
        resultado = servicio.eliminar_fila(int(self.navegacion.seEliminarInput.text()))
        if resultado == False:
            pass
        else:
            self.navegacion.seMensajeE.setText("Correcto")

    
    def buscar_tipo_ser(self):
        resultado = tipo_servi.mostrar_servicios_de_tipo(self.navegacion.tipoBuscar.text())
        if resultado:
            mensaje = f"\n--- {resultado} ---\n Servicios:\n"
            if resultado.servicios:
                for servicios in resultado.servicios:
                    mensaje += f"- {servicios.nombre}\n"
            else:
                print(" No tiene servicios registrados")

            self.navegacion.tResultadoS.setText(mensaje)

    def listar_servicio_segun_tipo(self):
        resultado = servicio.listar_servicio_y_tipo(self.navegacion.tipoBuscar.text())
        if resultado:
            mensaje = f"\nTIPO DE SERVICIO: {self.navegacion.tipoBuscar.text()}\n"
            for ts in resultado:  
                mensaje += f"\n{ts["servicio"]}: {ts['descservicio']}\nCosto renta: {ts['costo_renta']}\n"
                self.navegacion.tResultadoS.setText(mensaje)

    def buscar_tipoS_eli(self):
        resultado = tipo_servi.listar_tipos_servicio(self.navegacion.tipoBusqueda.text())
        if resultado:
            mensaje = f"\nTipo de servicios\n"
            for row in resultado:
                mensaje += f"\nCodigo del tipo: {row['codigoTiSer']}\nDescripcion del tipo: {row['descripcion']}\n"
            self.navegacion.tipoResultado.setText(mensaje)

    # Fin de la logica de servicios
    # Metodos para la logica de salones

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

    # Metodos para la logica de equipamientos
    
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


    # Metodos para la logica del trabajador

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
    
    # Fin de la logica del trabajador

    # Registro del Mobiliaro

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
        self.limpiar_caracteristicas()
        lay = self.navegacion.mobcont2.layout()
        cantidad = self.navegacion.seleccionCaracteristicas.value()
        for i in range(cantidad):
            label1 = QLabel(f"Característica {i+1}")
            label1.setStyleSheet("""
            QLabel {
                color: #000000;
            }
            """)
            lay.addWidget(label1)
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

            lay.addWidget(input_caracteristica)
            label2 = QLabel(f"Tipo de caracteristica {i+1}")
            label2.setStyleSheet("""
            QLabel {
                color: #000000;
            }
            """)
            lay.addWidget(label2)
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
            lay.addWidget(input_tipo_carac)
            self.inputs.append(input_caracteristica)
            self.inputs_tipo.append(input_tipo_carac)

            print("Yes")



    
    def mostrar_pagina(self, indice):
        self.navegacion.scrollAreaContenido.verticalScrollBar().setValue(0)
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    
    def registrar_cliente(self):
        tipo_cliente = ""
        if self.navegacion.cbTipoFisica.isChecked():
            tipo_cliente = "TCLPF"

        if self.navegacion.cbTipoMoral.isChecked():
            tipo_cliente= "TCLPM"

        resultado = cliente.registrar_clientes(self.navegacion.reRfc.text(), self.navegacion.reNombre.text(), self.navegacion.reApellPat.text(), self.navegacion.reApellMa.text(), self.navegacion.reNombreFiscal.text(), self.navegacion.reCorreo.text(), self.navegacion.reColonia.text(), self.navegacion.reCalle.text(), int(self.navegacion.reNumero.text()), tipo_cliente)

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

    def seleccionar_fisica(self, estado):
        if estado:
            self.navegacion.cbTipoMoral.setChecked(False)
            self.navegacion.reNombreFiscal.setEnabled(False)
            nombre_fiscal = f"{self.navegacion.reNombre.text()} {self.navegacion.reApellPat.text()} {self.navegacion.reApellMa.text()}"
            self.navegacion.reNombreFiscal.setText(nombre_fiscal)
            self.navegacion.clNombre.setText("Nombre")
            self.navegacion.clAp.setText("Apellido paterno")
            self.navegacion.clAm.setText("Apellido materno")

    def seleccionar_moral(self, estado):
        if estado:
            self.navegacion.cbTipoFisica.setChecked(False)
            self.navegacion.reNombreFiscal.setEnabled(True)
            self.navegacion.clNombre.setText("Nombre del contacto")
            self.navegacion.clAp.setText("Apellido paterno del contacto")
            self.navegacion.clAm.setText("Apellido materno del contacto")





    def cargar_seleccion_salon(self):
        self.navegacion.reSalonSelecc.clear()
        self.navegacion.reSalonSelecc.addItem("Selecciona un salon", None)
        obtener = salon.listar_salones()
        for sln in obtener:
            self.navegacion.reSalonSelecc.addItem(sln["nombre"], sln["numSalon"])
            print(sln["numSalon"])
    
    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
        print(salNumero)
        sali = self.buscar_usuario_por_id(salNumero)
        mensaje = "INFORMACION DEL SALON"
        mensaje += f"\n NOMBRE: {sali["nombre"]}"
        mensaje += f"\n COSTO: {str(sali["costoRenta"])}"
        self.subtotal_salon = 0.0
        self.subtotal_salon = sali["costoRenta"]
        if sali:
            self.navegacion.resultadoSalon.setText(mensaje)
    
    def buscar_usuario_por_id(self, salNumero):
        for s in salon.listar_salones():
            if s["numSalon"] == salNumero:
                return s
        return None

    def cargar_seleccion_tipoMontaje(self):
        self.navegacion.reTipoMontaje.clear()
        self.navegacion.reTipoMontaje.addItem("Selecciona un montaje", None)
        obtener = tipo_montaje.listar_tipos_montajes()
        for tm in obtener:
            self.navegacion.reTipoMontaje.addItem(tm["nombre"], tm["codigoMon"])
            print(tm["codigoMon"])
    
    def mostrar_info_montaje(self):
        tipoM = self.navegacion.reTipoMontaje.currentData()
        print(tipoM)
        tip = self.buscar_por_id(tipoM)
        mensaje = "INFORMACION DEL SALON"
        mensaje += f"\n NOMBRE: {tip["nombre"]}"
        mensaje += f"\n descripcion: {tip["descripcion"]}"
        if tip:
            self.navegacion.resultadoMontaje.setText(mensaje)

    def buscar_por_id(self, tipoM):
        for t in tipo_montaje.listar_tipos_montajes():
            if t["codigoMon"] == tipoM:
                return t
        return None






    def cargar_listas(self):
        self.navegacion.listaServicios.clear()
        # self.navegacion.listaEquipamiento.clear()

        for servi in servicio.listar_servicio():
            texto = f"{servi['nombre']} - ${servi['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, servi)
            self.navegacion.listaServicios.addItem(item)
    

    def calcular_subtotal_serv(self):
        servicios_seleccionados = self.navegacion.listaServicios.selectedItems()
        self.subtotal_servicios = 0.0

        for servicios in servicios_seleccionados:
            servicio = servicios.data(Qt.ItemDataRole.UserRole)
            self.subtotal_servicios += servicio["costoRenta"]
            
            numServicio = servicio['numServicio']
            print(numServicio)
            #enviar(numServicio)
        return self.subtotal_servicios

    def cargar_lista_equipamiento(self):
        self.navegacion.listaEquipamiento.clear()
        for equipa in equipamiento.listar_equipamentos():
            texto = f"{equipa['nombre']} - ${equipa['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, equipa)
            self.navegacion.listaEquipamiento.addItem(item)
    


    # Seccion del calendario


    def mostrar_controles_cantidad(self):
        self.limpiar_todos_controles()
        equipamientos_seleccionados = self.navegacion.listaEquipamiento.selectedItems()

        for equipamiento_item in equipamientos_seleccionados:
            # CORRECCIÓN CLAVE: Obtener el diccionario 'equipa' completo del rol UserRole
            equipa_data = equipamiento_item.data(Qt.ItemDataRole.UserRole) 

            # Verificar que los datos existen (buena práctica)
            if equipa_data is None:
                print("Error: El elemento seleccionado no contiene datos.")
                continue

            # Extraer las claves 'nombre' y 'costoRenta' del diccionario
            nombre = equipa_data['nombre'] # Asume que 'equipa' tiene la clave 'nombre'
            costoRenta = equipa_data['costoRenta'] # Asume que 'equipa' tiene la clave 'costoRenta'
            numEquipa = equipa_data['numEquipa']
            # Asegurar que el nombre no ha sido agregado ya (para evitar duplicados visuales)
            if nombre not in self.cantidades:
                # Inicializar la cantidad en 1 si es la primera vez que se agrega
                self.cantidades[nombre] = 1 
            
            self.crear_control_cantidad(nombre, costoRenta, numEquipa)

    def crear_control_cantidad(self, nombre, costoRenta, numEquipa):
        # Widget contenedor

        layEqui = self.navegacion.equipamientoW.layout()
        
        # Label del producto
        lbl_producto = QLabel(f"{nombre} (${costoRenta} c/u)")
        lbl_producto.setMinimumWidth(150)
        lbl_producto.setStyleSheet("""
            QLabel{
                color: #000000
            }
            """) 
        # Botón -
        btn_menos = QPushButton("-")
        btn_menos.setFixedSize(30, 30)
        btn_menos.clicked.connect(lambda: self.cambiar_cantidad(nombre, -1, numEquipa))
        btn_menos.setStyleSheet("""
            QPushButton{
                color: #ffffff;
                background-color: #000000;
            }                     
            """) 
        # Label cantidad actual
        lbl_cantidad = QLabel(str(self.cantidades[nombre]))
        lbl_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_cantidad.setMinimumWidth(30)
        lbl_cantidad.setStyleSheet("font-weight: bold; color: #000000;")
        
        # Botón R
        btn_mas = QPushButton("+")
        btn_mas.setFixedSize(30, 30)
        btn_mas.clicked.connect(lambda: self.cambiar_cantidad(nombre, 1, numEquipa))
        btn_mas.setStyleSheet("""
            QPushButton{
                color: #ffffff;
                background-color: #000000;
            }                     
            """) 

        # Label subtotal 

        #enviar(numEquipa, self.cantidades[nombre])
        subtotal = self.cantidades[nombre] * costoRenta

        lbl_subtotal = QLabel(f"${subtotal:.2f}")
        lbl_subtotal.setMinimumWidth(60)
        lbl_subtotal.setStyleSheet("font-weight: bold; color: blue;")

        if nombre not in self.controles_equipos:
            self.controles_equipos[nombre] = {
                'label_cantidad': lbl_cantidad,
                'label_subtotal': lbl_subtotal,
                'costo': costoRenta
            }

        sub = QLabel("Subtotal: ")
        sub.setStyleSheet("color: #000000;")
        # Agregar al layout
        layEqui.addWidget(lbl_producto)
        layEqui.addWidget(btn_menos)
        layEqui.addWidget(lbl_cantidad)
        layEqui.addWidget(btn_mas)
        layEqui.addWidget(sub)
        layEqui.addWidget(lbl_subtotal)
    

    def cambiar_cantidad(self, nombre, cambio, numEquipa):
        nueva_cantidad = self.cantidades[nombre] + cambio
        
        if nueva_cantidad < 0:
            return
        
        self.cantidades[nombre] = nueva_cantidad
        
        if nombre in self.controles_equipos:
            controles = self.controles_equipos[nombre]
            controles['label_cantidad'].setText(str(nueva_cantidad))

            self.datos_finales[numEquipa] = nueva_cantidad
            
            nuevo_subtotal = nueva_cantidad * controles['costo']
            controles['label_subtotal'].setText(f"${nuevo_subtotal:.2f}")
        
        self.calcular_total_general()
    # # 1. Actualizar la cantidad en el diccionario
    #     nueva_cantidad = self.cantidades[nombre] + cambio
    #     
    #     # 2. Validar que no sea menor a 0
    #     if nueva_cantidad < 0:
    #         return  # No hacer nada si sería negativo
    #     
    #     # 3. Guardar la nueva cantidad
    #     self.cantidades[nombre] = nueva_cantidad
    #     
    # Q    # 4. Actualizar los labels en la interfaz
    #     if nombre in self.controles_equipos:
    #         controles = self.controles_equipos[nombre]
    #         
    #         # Actualizar label de cantidad (ej: "1" → "2")
    #         controles['label_cantidad'].setText(str(nueva_cantidad))
    #         print(nueva_cantidad)
    #         print(numEquipa)
    #         # Calcular y actualizar subtotal
    #         nuevo_subtotal = nueva_cantidad * controles['costo']
    #         controles['label_subtotal'].setText(f"${nuevo_subtotal:.2f}")
    #     self.calcular_total_general()
    
    def registrar_reservacion(self):
        from gui.login import resultadoEmail
        fecha = self.navegacion.refecha.date().toPyDate()
        fechaReser = date.today()
        hora_inicio = self.navegacion.reHoraInicio.time().toString("HH:mm")
        hora_fin = self.navegacion.reHoraFin.time().toString("HH:mm")
        cliente = self.navegacion.reRfc.text()
        print(resultadoEmail[0])
        resultado = trabajador.obtener_rfc(resultadoEmail[0])
        print(resultado["rfc"])
        rfcTrabajador = resultado['rfc']
        descripEvento  = self.navegacion.reDescripcion.text()
        estimaAsistentes = self.navegacion.reEstimadoAsistentes.text()
        salon = self.navegacion.reSalonSelecc.currentText()
        tipo_montaje = self.navegacion.reTipoMontaje.currentText()

        lista_servicios = []
        servicios = self.navegacion.listaServicios.selectedItems()

        for item in servicios:
            data_servicio = item.data(Qt.ItemDataRole.UserRole)
            lista_servicios.append(data_servicio['nombre'])

        lista_equipamientos = [] 
        for num_equipo,cantidad in sorted(self.datos_finales.items()):
            equipa = ReserEquipamiento(num_equipo, cantidad)
            lista_equipamientos.append(equipa)

        resultado = reservacion.crear_reservacion(fechaReser, fechaEvento=fecha, horaInicio=hora_inicio, horaFin=hora_fin, descripEvento=descripEvento, estimaAsistentes=estimaAsistentes, tipo_montaje=tipo_montaje, trabajador=rfcTrabajador,datos_cliente=cliente, datos_salon=salon, equipamientos=lista_equipamientos, servicios=lista_servicios)

    
    def calcular_total_general(self):
        """Calcula el total de todos los equipos seleccionados"""
        total = 0
        
        # Sumar el subtotal de cada equipo
        for nombre, cantidad in self.cantidades.items():
            if nombre in self.controles_equipos:
                costo = self.controles_equipos[nombre]['costo']
                subtotal = cantidad * costo
                total += subtotal
        
        # Actualizar algún label de total en tu interfaz
        # Ejemplo: si tienes un label llamado lblTotalGeneral
        if hasattr(self.navegacion, 'lblTotalGeneral'):
            self.navegacion.lblTotalGeneral.setText(f"Total: ${total:.2f}")
        
        return total

    def total_reservacion(self):
        self.registrar_reservacion()
        subtotalServicios = self.calcular_subtotal_serv()
        subtotalEquipamiento = self.calcular_total_general()

        total = subtotalServicios + subtotalEquipamiento + self.subtotal_salon
        
        self.navegacion.reSubtotal.setText(f"Subtotal: {total}")
        self.navegacion.reIVA.setText(f"IVA: {total*0.16}")
        self.navegacion.reTotal.setText(f"Total: {total+(total*0.16)}")
        return total

    def limpiar_todos_controles(self):
        # Eliminar widgets del layout
        layEqui = self.navegacion.equipamientoW.layout()
        
        # Método 1: Eliminar todos los widgets del layout
        while layEqui.count():
            child = layEqui.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Limpiar diccionario de controles
        self.controles_equipos.clear()

    def actualizar_estado_mob(self):
        resultado = mobiliario.actu_esta_mob(int(self.navegacion.almNum.text()),int(self.navegacion.almCantidad.text()),self.navegacion.almEstadoAntiguo.text(), self.navegacion.almNuevoEstado.text())
        if resultado == False:
            self.navegacion.almMensaje.setText("Incorrecto")
        else:
            self.navegacion.almMensaje.setText("Correcto")
   

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
        resultado = equipamiento.obtener_equipa_estado(self.navegacion.almBuscadorE.text())
        if resultado == None:
            pass
        else:
            mensaje = "\n---EQUIPAMIENTOS---\n"
            for equi in resultado:
                mensaje += f"\nEquipamiento: {equi["Numero"]}.\nNombre: {equi["Nombre"]}.\nEstado Actual: {equi["Estado"]}\nCantidad: {equi["Cantidad"]}\n"
                self.navegacion.almResultadoE.setText(mensaje)

    def configurar_fechas_iniciales(self):
        hoy = date.today()
        self.fechas = [hoy + timedelta(days=i) for i in range (7)]

        self.navegacion.dateInicio.setDate(QDate.currentDate())
        self.navegacion.dateEvento_2.setDate(QDate.currentDate())

    def configurar_horario(self):
        self.horas = []
        for hora in range(7, 22):
            for minuto in [0, 30]:
                if hora == 20 and minuto == 30:
                    continue
                self.horas.append(f"{hora:02d}:{minuto:02d}")
        self.horas.append("22:00")

        self.navegacion.tableHorario.setRowCount(len(self.horas))
        self.navegacion.tableHorario.setColumnCount(len(self.fechas)+1)

        self.actualizar_encabezados()

        for i, hora in enumerate(self.horas):
            item = QTableWidgetItem(hora)
            item.setBackground(QColor(155, 88, 43))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.navegacion.tableHorario.setItem(i, 0, item)
            self.cargar_eventos()

    def actualizar_encabezados(self):
        headers = ["Hora"]
        for fecha in self.fechas:
            # Formato: "Lun 15/01"
            dia = fecha.strftime("%a")
            fecha_corta = fecha.strftime("%d/%m")
            headers.append(f"{dia}\n{fecha_corta}")
        
        self.navegacion.tableHorario.setHorizontalHeaderLabels(headers)
        self.navegacion.tableHorario.horizontalHeader().setStyleSheet("""
    QHeaderView::section {
        background-color: #9b582b;
        color: white;
        font-weight: bold;
        padding: 6px;
        border: 1px solid #9b582b;
    }
""") 
    def actualizar_fechas(self):
        """Actualizar las fechas mostradas en el horario"""
        fecha_inicio = self.navegacion.dateInicio.date().toPyDate()
        self.fechas = [fecha_inicio + timedelta(days=i) for i in range(7)]
        
        print(f"🔄 Actualizando fechas: {[f.strftime('%d/%m') for f in self.fechas]}")
        
        # Limpiar tabla (excepto columna de horas)
        self.limpiar_tabla()
        
        # Actualizar encabezados
        self.actualizar_encabezados()
        
        # Recargar eventos para las nuevas fechas
        self.cargar_eventos()
        
        QMessageBox.information(None, "Éxito", "Fechas actualizadas")

    def limpiar_tabla(self):
        """Limpiar la tabla (mantener solo columna de horas)"""
        for fila in range(self.navegacion.tableHorario.rowCount()):
            for columna in range(1, self.navegacion.tableHorario.columnCount()):
                self.navegacion.tableHorario.setItem(fila, columna, QTableWidgetItem(""))
        
    def agregar_evento(self):
        """Agregar nuevo evento"""
        try:
            # Obtener datos
            nombre = self.navegacion.inputNombre_2.text().strip()
            fecha = self.navegacion.dateEvento_2.date().toPyDate()
            hora_inicio = self.navegacion.timeInicio_2.time().toString("HH:mm")
            hora_fin = self.navegacion.timeFin_2.time().toString("HH:mm")
            
            print(f"➕ Intentando agregar evento: {nombre} | {fecha} | {hora_inicio}-{hora_fin}")
            
            # Validaciones simples
            if not nombre:
                QMessageBox.warning(None, "Error", "Ingresa un nombre para el evento")
                return
            
            if hora_inicio >= hora_fin:
                QMessageBox.warning(None, "Error", "La hora de fin debe ser mayor a la de inicio")
                return
            
            # Verificar que la fecha esté en el rango mostrado
            if fecha not in self.fechas:
                QMessageBox.warning(None, "Error", 
                                  f"La fecha {fecha.strftime('%d/%m/%Y')} debe estar en el rango mostrado")
                return
            
            # Verificar que las horas estén en el rango
            if hora_inicio not in self.horas or hora_fin not in self.horas:
                QMessageBox.warning(None, "Error", 
                                  f"Las horas deben estar entre 19:00 y 22:00")
                return
            
            # Verificar disponibilidad
            if not self.verificar_disponibilidad(fecha, hora_inicio, hora_fin):
                QMessageBox.warning(None, "Conflicto", 
                                  "Ya hay un evento en ese horario")
                return
            
            # Guardar en base de datos simulada
            evento = db.agregar_evento(nombre, fecha, hora_inicio, hora_fin)
            print(f"✅ Evento guardado en BD: {evento}")
            
            # Actualizar horario
            self.marcar_evento_en_horario(evento)
            
            # Limpiar formulario
            self.navegacion.inputNombre_2.clear()
            
            QMessageBox.information(None, "Éxito", 
                                  f"Evento '{nombre}' agregado para {fecha.strftime('%d/%m/%Y')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            QMessageBox.critical(None, "Error", f"Error: {str(e)}")
    
    def verificar_disponibilidad(self, fecha, hora_inicio, hora_fin):

        eventos_fecha = db.obtener_eventos_por_fecha(fecha)

        
        for evento in eventos_fecha:
            if not (hora_fin <= evento['hora_inicio'] or hora_inicio >= evento['hora_fin']):
                print(f"❌ Conflicto con evento: {evento}")
                return False
        return True

    def cargar_eventos(self):
        """Cargar todos los eventos en el horario"""
        todos_eventos = db.obtener_todos_eventos()
        print(f"📂 Cargando {len(todos_eventos)} eventos en el horario")
        
        for evento in todos_eventos:
            if evento['fecha'] in self.fechas:
                print(f"  - Marcando evento: {evento}")
                self.marcar_evento_en_horario(evento)

    def marcar_evento_en_horario(self, evento):
        """Marcar un evento en el horario"""
        try:
            # Encontrar posición en la tabla
            fila_inicio = self.horas.index(evento['hora_inicio'])
            fila_fin = self.horas.index(evento['hora_fin'])
            columna = self.fechas.index(evento['fecha']) + 1
            
            print(f"  🎯 Marcando en: fila {fila_inicio}-{fila_fin}, columna {columna}")
            
            # Marcar celdas
            for fila in range(fila_inicio, fila_fin):
                item = QTableWidgetItem(evento['nombre'])
                item.setBackground(QBrush(QColor(155, 88, 43)))  # Azul
                item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Guardar ID del evento para poder identificarlo
                item.setData(Qt.ItemDataRole.UserRole, evento['id'])
                
                self.navegacion.tableHorario.setItem(fila, columna, item)
                print(f"    ✅ Celda [{fila}, {columna}] marcada: {evento['nombre']}")
                
        except ValueError as e:
            print(f"⚠️ Error marcando evento {evento}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def celda_doble_clic(self, fila, columna):
        """Manejar doble clic en celdas para eliminar eventos"""
        if columna == 0:  # Columna de horas
            return
        
        item = self.navegacion.tableHorario.item(fila, columna)
        if item and item.data(Qt.ItemDataRole.UserRole):
            evento_id = item.data(Qt.ItemDataRole.UserRole)
            evento = next((e for e in db.obtener_todos_eventos() if e['id'] == evento_id), None)
            
            if evento:
                respuesta = QMessageBox.question(
                    self, "Eliminar Evento", 
                    f"¿Eliminar evento?\n\n"
                    f"📝 {evento['nombre']}\n"
                    f"📅 {evento['fecha'].strftime('%d/%m/%Y')}\n"
                    f"⏰ {evento['hora_inicio']} - {evento['hora_fin']}",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if respuesta == QMessageBox.StandardButton.Yes:
                    db.eliminar_evento(evento_id)
                    self.actualizar_fechas()  # Recargar el horario
                    QMessageBox.information(self, "Éxito", "Evento eliminado")

    def mostrar_eventos(self):
        """Mostrar todos los eventos en un mensaje"""
        eventos = db.obtener_todos_eventos()
        
        if not eventos:
            QMessageBox.information(self, "Eventos", "No hay eventos programados")
            return
        
        mensaje = "📅 TODOS LOS EVENTOS:\n\n"
        for evento in sorted(eventos, key=lambda x: (x['fecha'], x['hora_inicio'])):
            mensaje += (f"• {evento['nombre']}\n"
                       f"  📍 {evento['fecha'].strftime('%A %d/%m/%Y')}\n"
                       f"  ⏰ {evento['hora_inicio']} - {evento['hora_fin']}\n\n")
        
        QMessageBox.information(None, "Eventos Guardados", mensaje)
    
    def limpiar_horario(self):
        """Limpiar todo el horario y la base de datos"""
        respuesta = QMessageBox.question(
            self, "Confirmar", 
            "¿Estás seguro de que quieres eliminar TODOS los eventos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            db.limpiar_base_datos()
            self.limpiar_tabla()
            QMessageBox.information(None, "Éxito", "Todos los eventos han sido eliminados")
    
    def volver_login(self, link):
        from gui.login import Login
        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
