import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db_settings import BaseDeDatos
from models.TipoServicio import TipoServicio
from repositories_crud.TipoServiciosRepository import TipoServiciosRepository

class TipoServicioService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.repository = TipoServiciosRepository(self.db)

    def prueba(self):
        p = self.repository.descripcion_de_tipo("Empresarial")
        print(p[0])
        

ins = TipoServicioService()
ins.prueba()
