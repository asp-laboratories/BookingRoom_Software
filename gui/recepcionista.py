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
ruta_ui = Path(__file__).parent / "recepcionista.ui"

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



class Recepcionista():
    def __init__(self):
        self.navegacion = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)
        


        self.navegacion.subMenuRecepcion.setVisible(False)
        # self.navegacion.widget.layout()

        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)

        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(6))





       
        self.navegacion.reConfirmar.clicked.connect(self.total_reservacion)
        


        
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

    def volver_login(self, link):
        from gui.login import Login
        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
