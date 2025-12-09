from config.db_settings import BaseDeDatos
from models.Trabajador import Trabajador
from repositories_crud.RolRepository import RolRepository
from repositories_crud.TrabajadorRepository import TrabajadorRepository


class TrabajadorServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.trabajador_repository = TrabajadorRepository(self.db)
        self.rol_repository = RolRepository(self.db)
       
    def registrar_trabajadores(self, rfc, numTrabajador, nombre, priApellido, segApellido, email):
        trabajador = Trabajador(rfc, numTrabajador, nombre, priApellido, segApellido, email)
        return self.trabajador_repository.crear_trabajador(trabajador)

    def listar_trabajadores(self):
        print("Trabajadores: ")
        return self.trabajador_repository.listar_trabajador()
        # print("Nombre:\t Rol:\t")
        # for row in trabajador:
            # print(f"{row['nombre']}\t {row['rol']}")

    def obtener_nombre(self, nombre):
        return self.trabajador_repository.sacar_trabajador(nombre)
        
    def actualizar_roles(self, RFC, codigoRolValor):
        descripcionRol = self.rol_repository.obtener_descripcion(codigoRolValor)
        self.trabajador_repository.actualizar_rol(RFC, descripcionRol.codigoRol)
    
    def buscar_al_trabajador(self, buscador):
        return self.trabajador_repository.buscar_trabajadores(buscador)
    
    def buscar_al_trabajador_reserva(self, buscador):
        return self.trabajador_repository.buscar_trabajadores_por_reservacion(buscador)

    def obtener_rfc_nombre(self, nombre):
        rfc = self.trabajador_repository.obtener_rfc(nombre)
        return rfc['rfc']
