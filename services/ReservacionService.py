
from config.db_settings import BaseDeDatos
from repositories_crud.ReservacionRepository import ReservacionRepository
from models.Reservacion import Reservacion

class ReservacionService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database='BookingRoomLocal')
        self.repository = ReservacionRepository(db)

    # Metodos
    def crear_reservacion(self, fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes, tipo_montaje, trabajador, datos_cliente, datos_salon, equipamientos, servicios):
        # Comprobaciones del tipo de montaje, servicios, equipamientos, datos_salon, trabajador
        # Se tienen que agregar como pk
        reservacion = Reservacion(fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes,)