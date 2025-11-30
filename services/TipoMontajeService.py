from config.db_settings import BaseDeDatos
from repositories_crud.TipoMontajeRepository import TipoMontajeRepository

class TipoMontajeService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database='BookingRoomLocal')
        self.TipoMontajeRepository = TipoMontajeRepository(db)

    # Metodos
    def listar_tipos_montajes(self):
        tipos_montajes = self.TipoMontajeRepository.listar_tipos_montajes()
        return tipos_montajes