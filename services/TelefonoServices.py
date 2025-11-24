from config.db_settings import BaseDeDatos
from models.Telefonos import Telefonos
from repositories_crud.TelefonoRepository import TelefonoRepository


class TelefonoServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.telefono_repository = TelefonoRepository(self.db)
       
    def registrar_telefono(self, tel, datos_cliente, trabajador):
        telefono = Telefonos(tel, datos_cliente, trabajador)
        return self.telefono_repository.crear_telefono(telefono)

    def listar_telefonos(self):
        print("Telefonos: ")
        telefono = self.telefono_repository.listar_telefono()
        print("Telefono:\t Cliente:\t Trabajador:")
        for row in telefono:
            print(f"{row['telefono']}\t\t\t {row['datos_cliente']}\t\t\t {row['trabajador']}")

