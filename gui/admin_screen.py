from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QMessageBox,
)
from datetime import date, timedelta
from gui.registro_cliente import RegistroCliente
from services.DatosClienteService import DatosClienteService
from services.ReserEquipaService import ReserEquipaService
from services.ReservacionService import ReservacionService
from services.SalonServices import SalonServices
from services.ServicioServices import ServicioService
from services.EquipamentoService import EquipamentoService
from services.TelefonoServices import TelefonoServices
from services.TipoEquipamientoService import TipoEquipamentoService
from services.TipoMobiliarioService import TipoMobiliarioService
from services.TipoMontajeService import TipoMontajeService
from services.TipoServicioService import TipoServicioService
from services.TrabajadorServices import TrabajadorServices
from services.mobiliarioService import mobiliarioService
from services.PagoService import PagoServices
from services.DatosMontajeService import DatosMontajeService
from services.RolService import RolService
from services.TipoClienteService import TipoClienteService
from gui.handlers.service_handler import ServiceHandler
from gui.handlers.salon_handler import SalonHandler
from gui.handlers.equipment_handler import EquipmentHandler
from gui.handlers.mobiliario_handler import MobiliarioHandler
from gui.handlers.worker_handler import WorkerHandler
from gui.handlers.client_handler import ClientHandler
from gui.handlers.pago_handler import PagoHandler
from gui.handlers.reservacion_handler import ReservacionHandler
from gui.handlers.horario_handler import HorarioHandler
ruta_ui = Path(__file__).parent / "admin_screen.ui"

obtenerNumeroReservacion = []


class AdministradorScreen:
    def __init__(self, db_instance, trabajador):
        self.trabajador_actual = trabajador
        # Se recibe y se guarda la instancia única de la BD
        self.db = db_instance

        # Se inicializan todos los servicios pasando la misma instancia de la BD
        self.tipo_servi = TipoServicioService(self.db)
        self.servicio = ServicioService(self.db)
        self.salon = SalonServices(self.db)
        self.equipamiento = EquipamentoService(self.db)
        self.trabajador = TrabajadorServices(self.db)
        self.cliente = DatosClienteService(self.db)
        self.datosMontaje = DatosMontajeService(self.db)
        self.telefono = TelefonoServices(self.db)
        self.mobiliario = mobiliarioService(self.db)
        self.tipo_montaje = TipoMontajeService(self.db)
        self.reservacion = ReservacionService(self.db)
        self.reser_equipa = ReserEquipaService(self.db)
        self.pagos = PagoServices(self.db)
        self.tipo_mobiliario = TipoMobiliarioService(self.db)
        self.TrabajadorRol = RolService(self.db)
        self.TipoCliente = TipoClienteService(self.db)
        self.tipo_equipamiento = TipoEquipamentoService(self.db)

        self.navegacion = uic.loadUi(str(ruta_ui))

        # Instantiation of handlers (estos no necesitan la BD directamente)
        self.service_handler = ServiceHandler(self)
        self.salon_handler = SalonHandler(self)
        self.equipment_handler = EquipmentHandler(self)
        self.mobiliario_handler = MobiliarioHandler(self)
        self.worker_handler = WorkerHandler(self)
        self.client_handler = ClientHandler(self)
        self.pago_handler = PagoHandler(self)
        self.reservacion_handler = ReservacionHandler(self)
        self.horario_handler = HorarioHandler(self)

        # self.initGUI()
        self.navegacion.show()
        self.navegacion.linkLogin.linkActivated.connect(self.volver_login)

        # Mensaje para evaluar las operaciones

        # Ocultamiento de los submenus de los tres apartados
        self.navegacion.subMenuAdministracion.setVisible(False)
        self.navegacion.subMenuAlmacen.setVisible(False)
        self.navegacion.subMenuRecepcion.setVisible(False)
        # self.navegacion.widget.layout()

        # Abrir las subopciones
        self.navegacion.btnAdministracion.clicked.connect(self.abrir_opciones_admin)
        self.navegacion.btnAlmacen.clicked.connect(self.abrir_opciones_almac)
        self.navegacion.btnRecepcion.clicked.connect(self.abrir_opciones_recep)

        # Navegacion entre paginas
        self.navegacion.servicios.clicked.connect(lambda: self.mostrar_pagina(1))
        self.navegacion.equipamiento.clicked.connect(lambda: self.mostrar_pagina(2))
        self.navegacion.salon.clicked.connect(lambda: self.mostrar_pagina(3))
        self.navegacion.mobiliario_2.clicked.connect(lambda: self.mostrar_pagina(4))
        self.navegacion.subTrabajador.clicked.connect(lambda: self.mostrar_pagina(5))
        self.navegacion.reservacion.clicked.connect(lambda: self.mostrar_pagina(6))
        self.navegacion.mobiliario.clicked.connect(lambda: self.mostrar_pagina(7))
        self.navegacion.pagos.clicked.connect(lambda: self.mostrar_pagina(8))
        self.navegacion.reSalon.clicked.connect(lambda: self.mostrar_pagina(11))
        # self.navegacion.horario.clicked.connect(lambda: self.mostrar_pagina(12))
        # =========================================================================================
        # CONEXIONES DE HORARIO
        # =========================================================================================
        # NOTA: Asegúrate de que los nombres de widgets en tu .ui coincidan.
        self.navegacion.btnActualizarHorario.clicked.connect(self.horario_handler.actualizar_vista_horario)
        self.navegacion.comboSalonHorario.currentIndexChanged.connect(self.horario_handler.actualizar_vista_horario)
        self.navegacion.dateInicioHorario.dateChanged.connect(self.horario_handler.actualizar_vista_horario)
        
        # Conexiones para navegar entre semanas (asegúrate de que los botones existan en el .ui)
        self.navegacion.btnSiguienteSemana.clicked.connect(self.horario_handler.avanzar_semana)
        self.navegacion.btnAnteriorSemana.clicked.connect(self.horario_handler.retroceder_semana)
        # =========================================================================================

        # Botones de los eventos de servicios
        self.navegacion.sConfirmar.clicked.connect(
            self.service_handler.intentar_registrar_servicio
        )
        # Botones para los eventos de equipamiento
        self.navegacion.eConfirmar.clicked.connect(
            self.equipment_handler.intentar_registrar_equipamiento
        )
        # Botones para los eventos de salones
        self.navegacion.saConfirmar.clicked.connect(
            self.salon_handler.intentar_registrar_salon
        )
        # Botones para los eventos de mobiliario
        self.navegacion.amConfirmar.clicked.connect(
            self.mobiliario_handler.generar_caracteristicas
        )
        self.navegacion.amConfirmar_2.clicked.connect(
            self.mobiliario_handler.intentar_registrar_mobiliario
        )

        # Botones para los eventos de trabajadores
        self.navegacion.atConfirmar.clicked.connect(
            self.worker_handler.intentar_establecer_rol
        )
        self.navegacion.atBuscar.clicked.connect(self.worker_handler.buscar_trabajadores_y_mostrar)
        self.navegacion.atBuscar_2.clicked.connect(
            self.worker_handler.buscar_sus_reservaciones
        )

        self.navegacion.reConfirmar.clicked.connect(
            self.reservacion_handler.intentar_registrar_reservacion
        )
        # Assuming a button named reCalcularTotal exists in the UI
        # self.navegacion.reCalcularTotal.clicked.connect(
        #     self.reservacion_handler.total_reservacion
        # )

        # Botones para los eventos de actualizacion de roles por parte del almacenista
        self.navegacion.almConfirmarMobi_3.clicked.connect(
            self.mobiliario_handler.intentar_actualizar_estado_manual_mob
        )
        self.navegacion.almConfirmar_2.clicked.connect(
            self.equipment_handler.intentar_actualizar_estado_manual # Nueva función para actualizar desde la tabla
        )
        # Carga el ComboBox de estados de equipamiento al iniciar y conecta la búsqueda automática
        self.equipment_handler.cargar_estados_equipamiento()
        self.navegacion.almBuscadorE.currentIndexChanged.connect(
            self.equipment_handler.buscar_estado_equipamiento
        )

        self.navegacion.buscarCliente.clicked.connect(
            self.client_handler.buscar_cliente
        )
        self.navegacion.registrarCliente.setVisible(False)

        self.equipment_handler.cargar_tipos_equipamiento_registro()
        self.mobiliario_handler.cargar_seleccion_tipoMobiliario()
        self.navegacion.reMontajeInfo.clicked.connect(
            self.reservacion_handler.mostrar_info_montaje
        )
        # Eventos de salones, equipamiento y servicios dentro de reservacion
        self.salon_handler.cargar_seleccion_salon()
        self.salon_handler.cargar_seleccion_estado_salon()
        self.navegacion.reSalonInfo.clicked.connect(
            self.salon_handler.mostrar_info_salon
        )
        self.reservacion_handler.cargar_listas()
        self.equipment_handler.cargar_lista_equipamiento()
        self.navegacion.listaEquipamiento.itemSelectionChanged.connect(
            self.reservacion_handler.mostrar_controles_cantidad
        )

        self.service_handler.cargar_tipos_servicios()
        self.equipment_handler.cargar_tipos_equipamiento()
        # Variables utilizadas para almacenar informatcion

        self.navegacion.buscarTipo_3.clicked.connect(
            self.reservacion_handler.obtener_fecha_reser
        )

        self.worker_handler.llenar_combox_roles()
        self.navegacion.rolBuscarTrabajadores.clicked.connect(
            self.worker_handler.llenar_lista_trabajadores
        )
        self.navegacion.rolTrabajadores.itemClicked.connect(
            self.worker_handler.detalles_trabajador
        )

        self.navegacion.clPersonaFisica.toggled.connect(
            self.client_handler.mostrar_clientes_por_tipo
        )
        self.navegacion.clClientesTipo.itemClicked.connect(
            self.client_handler.detalle_cliente
        )

        self.subtotal_servicios = 0.0
        self.subtotal_salon = 0.0
        self.fechas = []

        # Controles del calendario

        # Botonoes modulo de pagos
        self.navegacion.pagosBuscar.clicked.connect(
            self.pago_handler.buscar_historial_pagos
        )
        self.navegacion.reNumReser.textChanged.connect(
            self.pago_handler.mostrar_descripcion_en_tiempo_real
        )
        self.navegacion.reConfirmar_2.clicked.connect(
            self.pago_handler.intentar_registrar_pago
        )
        self.navegacion.reCancelar_2.clicked.connect(self.pago_handler.limpiar_pago)

        # Combobox del tipo de montaje en reservacion
        self.navegacion.reSalonSelecc.currentIndexChanged.connect(
            self.reservacion_handler.cargar_seleccion_tipoMontaje
        )
        self.navegacion.reSalonSelecc.currentIndexChanged.connect(
            self.salon_handler.actualizar_subtotal_salon_y_total
        )
        self.navegacion.reTipoMontaje.currentIndexChanged.connect(
            self.reservacion_handler.total_reservacion
        )
        self.navegacion.listaServicios.itemSelectionChanged.connect(
            self.reservacion_handler.total_reservacion
        )

        self.navegacion.registrarCliente.clicked.connect(
            self.client_handler.abrir_registro_cliente
        )
        # Metodos para abrir las subopciones

        # =========================================================================================
        # MÉTODOS DE NAVEGACIÓN Y UI
        # =========================================================================================

    def abrir_opciones_admin(self):
        self.navegacion.subMenuAdministracion.setVisible(
            not self.navegacion.subMenuAdministracion.isVisible()
        )

    def abrir_opciones_almac(self):
        self.navegacion.subMenuAlmacen.setVisible(
            not self.navegacion.subMenuAlmacen.isVisible()
        )

    def abrir_opciones_recep(self):
        self.navegacion.subMenuRecepcion.setVisible(
            not self.navegacion.subMenuRecepcion.isVisible()
        )

    def abrir_registro_cliente(self):
        self.cliente = RegistroCliente()
        # Seccion de servicios - logica de servicios

    def mostrar_pagina(self, indice):
        self.navegacion.scrollAreaContenido.verticalScrollBar().setValue(0)
        self.navegacion.stackedWidget.setCurrentIndex(indice)

    def volver_login(self, link):
        from gui.login import Login

        if link == "cerrar":
            self.navegacion.hide()
            self.login = Login(self.db)

    def mostrar_confirmacion(self, titulo: str, mensaje: str) -> bool:
        reply = QMessageBox.question(
            None,
            titulo,
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes
