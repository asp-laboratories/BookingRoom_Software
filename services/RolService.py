from config.db_settings import BaseDeDatos
from models.Rol import Rol
from repositories_crud.RolRepository import RolRepository


class RolService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
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
        return rol

    def obtener_codigo_rol(self, rolDescripcion):
        rolCodigo = self.rol_repository.obtener_codigo_rol(rolDescripcion)
        if not rolCodigo:
            print("Algo salio mal, no tenemos un codigo de rol")
            return None
        else:
            return rolCodigo['codigoRol']

    def obtener_trabajadores_rol(self, rol):
        codigRol = self.obtener_codigo_rol(rol)

        info_trabajadores = self.rol_repository.trabajadores_rol(codigRol)

        trabajadores = []
        
        aux_traba = []
        for traba in info_trabajadores:
            if traba['nombre'] not in aux_traba:
                aux_traba.append(traba['nombre'])
                trabajador = {
                    'nombre'    : traba['nombre'],
                    'numTraba'  : traba['numTraba'],
                    'RFC'       : traba['RFC'],
                    'email'     : traba['email'],
                    'telefonos' : []
                }
                trabajador['telefonos'].append(traba['telefono'])

                trabajadores.append(trabajador)
            
            else:
                for traba2 in trabajadores:
                    if traba2['nombre'] == traba['nombre']:
                        traba2['telefonos'].append(traba['telefono'])

        return trabajadores



    # def listar_servicio_y_tipo(self):
    #
    #     servicios = self.servicio_repository.obtener_servicios_inner()
    #     if servicios:
    #         for ser in servicios:
    #             print(f"Informacion de: {ser.nombre}:\n{ser.descripcion}\n{ser.costo_renta}\n{ser.tipo_nombre}")
