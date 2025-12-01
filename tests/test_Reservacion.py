
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ReservacionService import ReservacionService
from models.ReserEquipa import ReserEquipamiento

reservacion = ReservacionService()

def crear_reservacion():
    equipam1 = ReserEquipamiento('microfono inalambrico', 1)
    equipam2 = ReserEquipamiento('tv', 2)
    equipamientos = []
    servicios = []
    reservacion.crear_reservacion('2020-01-02', '2020-02-03', '10:10:10', '10:10:10', "Cosa", 10, 'montaje imperial', 'juanito', 'hector mendoza', 'chopin', equipamientos, servicios)

if __name__ == "__main__":
    crear_reservacion()

