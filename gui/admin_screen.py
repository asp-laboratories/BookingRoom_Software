import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QListWidgetItem, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from models.MobCarac import MobCarac
from services.DatosClienteService import DatosClienteServices
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TelefonoServices import TelefonoServices
from services.TrabajadorServices import TrabajadorServices
from services.mobiliarioService import mobiliarioService
from utils.Formato import permitir_ingreso
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
        self.navegacion.mobiliario_2.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))
        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(6))

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
       
        self.navegacion.reConfirmar.clicked.connect(self.total_reservacion)
        
        self.navegacion.almConfirmar.clicked.connect(self.actualizar_estado_mob)

        self.navegacion.clienteConfirmar.clicked.connect(self.registrar_cliente)
        self.deshabilitar_telefonos()
        self.navegacion.cbTelefono2.toggled.connect(self.ingresar_segundoTel)
        self.navegacion.cbTelefono3.toggled.connect(self.ingresar_tercerTel)
        
        self.navegacion.cbTipoFisica.toggled.connect(self.seleccionar_fisica)
        self.navegacion.cbTipoMoral.toggled.connect(self.seleccionar_moral)
        
        

        self.cargar_seleccion_salon()
        self.navegacion.reSalonInfo.clicked.connect(self.mostrar_info_salon)
        self.cargar_listas()
        self.cargar_lista_equipamiento()
        self.navegacion.listaEquipamiento.itemSelectionChanged.connect(self.mostrar_controles_cantidad)
        #self.navegacion.btnSubTotalE.clicked.connect(self.calcular_equipamiento)
        
        self.subtotal_servicios = 0.0
        self.subtotal_salon = 0.0 
        self.cantidades = {}
        self.controles_equipos = {}
        self.inputs = []
        self.inputs_tipo = []

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(not self.navegacion.subMenuAdministracion.isVisible())
    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(not self.navegacion.subMenuAlmacen.isVisible())
    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(not self.navegacion.subMenuRecepcion.isVisible())

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
    
    def mostrar_info_salon(self):
        salNumero = self.navegacion.reSalonSelecc.currentData()
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

        return self.subtotal_servicios

    def cargar_lista_equipamiento(self):
        self.navegacion.listaEquipamiento.clear()
        for equipa in equipamiento.listar_equipamentos():
            texto = f"{equipa['nombre']} - ${equipa['costoRenta']:.2f}"
            item = QListWidgetItem(texto)
            item.setData(Qt.ItemDataRole.UserRole, equipa)
            self.navegacion.listaEquipamiento.addItem(item)
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

            # Asegurar que el nombre no ha sido agregado ya (para evitar duplicados visuales)
            if nombre not in self.cantidades:
                # Inicializar la cantidad en 1 si es la primera vez que se agrega
                self.cantidades[nombre] = 1 
            
            self.crear_control_cantidad(nombre, costoRenta)

    def crear_control_cantidad(self, nombre, costoRenta):
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
        btn_menos.clicked.connect(lambda: self.cambiar_cantidad(nombre, -1))
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
        btn_mas.clicked.connect(lambda: self.cambiar_cantidad(nombre, 1))
        btn_mas.setStyleSheet("""
            QPushButton{
                color: #ffffff;
                background-color: #000000;
            }                     
            """) 

        # Label subtotal
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
    
    def cambiar_cantidad(self, nombre, cambio):

    # 1. Actualizar la cantidad en el diccionario
        nueva_cantidad = self.cantidades[nombre] + cambio
        
        # 2. Validar que no sea menor a 0
        if nueva_cantidad < 0:
            return  # No hacer nada si sería negativo
        
        # 3. Guardar la nueva cantidad
        self.cantidades[nombre] = nueva_cantidad
        
        # 4. Actualizar los labels en la interfaz
        if nombre in self.controles_equipos:
            controles = self.controles_equipos[nombre]
            
            # Actualizar label de cantidad (ej: "1" → "2")
            controles['label_cantidad'].setText(str(nueva_cantidad))
            
            # Calcular y actualizar subtotal
            nuevo_subtotal = nueva_cantidad * controles['costo']
            controles['label_subtotal'].setText(f"${nuevo_subtotal:.2f}")
        self.calcular_total_general()

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
    

    def volver_login(self, link):
        from gui.login import Login
        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login()

    # def initGUI(self):
    #     self.login.btnIniciar.clicked.connect(self.ingresar)
