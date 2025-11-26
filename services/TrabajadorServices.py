from config.db_settings import BaseDeDatos
from models.Trabajador import Trabajador
from repositories_crud.TrabajadorRepository import TrabajadorRepository


class TrabajadorServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.trabajador_repository = TrabajadorRepository(self.db)
       
    def registrar_trabajadores(self, rfc, numTrabajador, nombre, priApellido, segApellido, email):
        trabajador = Trabajador(rfc, numTrabajador, nombre, priApellido, segApellido, email)
        return self.trabajador_repository.crear_trabajador(trabajador)

    def listar_trabajadores(self):
        print("Trabajadores: ")
        return self.trabajador_repository.listar_trabajador()
        # print("Nombre:\t Rol:\t")
        # for row in trabajador:
            # print(f"{row['nombre']}\t {row['rol']}")

    def actualizar_trabajadores(self, RFC, codigoRol):
        self.trabajador_repository.actualizar_trabajadores(RFC, codigoRol)
    
    def buscar_al_trabajador(self, buscador):
        return self.trabajador_repository.buscar_trabajadores(buscador)
