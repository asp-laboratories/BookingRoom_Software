
from config.db_settings import BaseDeDatos
from repositories_crud.ReservacionRepository import ReservacionRepository
from models.Reservacion import Reservacion
from TipoMontajeService import TipoMontajeService
from services.TrabajadorServices import TrabajadorServices
from services.DatosClienteService import DatosClienteService
from services.

class ReservacionService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database='BookingRoomLocal')
        self.reservacion_repository = ReservacionRepository(db)
        self.tipo_montajeService = TipoMontajeService(db)
        self.TrabajadorService = TrabajadorServices(db)
        self.DatosClienteServices = DatosClienteService(db)

    # Metodos
    def crear_reservacion(self, fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes, tipo_montaje, trabajador, datos_cliente, datos_salon, equipamientos, servicios):
        # Comprobaciones del tipo de montaje, servicios, equipamientos, datos_salon, trabajador
        # Se tienen que agregar como pk
        numDatMon = self.tipo_montajeService.obtener_datos_montaje(tipo_montaje=tipo_montaje, datos_salon=datos_salon)
        rfcTraba = self.TrabajadorService.obtener_rfc(trabajador)
        rfcCliente = self.DatosClienteServices.obtener_rfc(datos_cliente)
        reservacion = Reservacion(fechaReser=fechaReser, fechaEvento=fechaEvento, horaInicio=horaInicio, horaFin=horaFin, descripEvento=descripEvento, estimaAsistentes=estimaAsistentes, datos_montaje=numDatMon, trabajador=rfcTraba, datos_cliente=rfcCliente, equipamientos=equipamientos, servicios=servicios)

        return self.reservacion_repository.registrar_reservacion(reservacion)