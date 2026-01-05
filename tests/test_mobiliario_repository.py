import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories_crud.MobiliarioRepository import MobiliarioRepository
from config.db_settings import BaseDeDatos


if __name__ == "__main__":
    conexcion = BaseDeDatos(database="BookingRoomLocal")
    prueba = MobiliarioRepository(conexcion)
    # This will fail as it is now. It needs a proper connection.
    # print(prueba.obtener_esta_mob(1, "dispo"))
