from repositories_crud.DatosMontajeRepository import DatosMontajeRepository
from services.TipoMontajeService import TipoMontajeService
from config.db_settings import BaseDeDatos


class DatosMontajeService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database="BookingRoomLocal")
        self.db = db
        self.TipoMontajeRepository = TipoMontajeService()
        self.DatosMontajeRepository = DatosMontajeRepository(self.db)

    # Metodos
    def mobiliarios_montaje(self, tipo_montaje, datos_salon):
        numDatMon = self.TipoMontajeRepository.obtener_datos_montaje(
            tipo_montaje, datos_salon
        )

        mobiliarios = self.DatosMontajeRepository.mobiliarios_montaje(numDatMon)

        return mobiliarios
