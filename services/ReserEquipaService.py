from config.db_settings import BaseDeDatos
from repositories_crud.ReserEquiRepository import ReserEquiRepository


class ReserEquipaService:
    def __init__(self, db_instance):
        self.db = db_instance
        self.reserE = ReserEquiRepository(self.db)

    def crear_equipamiento_en_reser(self, reservacion, equipamiento, cantidad):
        return self.reserE.crear_reservacion_equipa(reservacion, equipamiento, cantidad)
