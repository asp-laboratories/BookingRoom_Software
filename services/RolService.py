from config.db_settings import BaseDeDatos
from models.Rol import Rol
from repositories_crud.RolRepository import RolRepository


class RolService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.rol_repository = RolRepository(self.db)
       
    def registrar_rol(self, codigoRol, descripcion):
        rol = Rol(codigoRol, descripcion)
        return self.rol_repository.crear_rol(rol)

    def listar_rol(self):
        print("Roles: ")
        rol = self.rol_repository.listar_rol()
        print("Codigo:\t Descripcion:\t")
        for row in rol:
            print(f"{row['codigoRol']}\t {row['descripcion']}")

    # def listar_servicio_y_tipo(self):
    #
    #     servicios = self.servicio_repository.obtener_servicios_inner()
    #     if servicios:
    #         for ser in servicios:
    #             print(f"Informacion de: {ser.nombre}:\n{ser.descripcion}\n{ser.costo_renta}\n{ser.tipo_nombre}")
