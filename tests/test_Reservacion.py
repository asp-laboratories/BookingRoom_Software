import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ReservacionService import ReservacionService
from models.ReserEquipa import ReserEquipamiento

reservacion = ReservacionService()


def crear_reservacion():
    equipamientos = [
        ReserEquipamiento("microfono inalambr", 1),
        ReserEquipamiento("tv", 2),
    ]
    servicios = []
    reservacion.crear_reservacion(
        "2020-01-02",
        "2020-02-03",
        "10:10:10",
        "10:10:10",
        "Cosa",
        10,
        "montaje imperial",
        "María",
        "hector mendoza",
        "chopin",
        equipamientos,
        servicios,
    )


def obtener_info_reservacion():
    reser = reservacion.info_reservacion(44)
    print(
        f"Numero de Reservacion: {reser['numReser']} | Fecha de Reservacion: {reser['fechaReser']}"
    )


if __name__ == "__main__":
    crear_reservacion()
