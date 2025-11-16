from config.db_settings import BaseDeDatos
from models.Servicios import Servicio
from repositories_crud.ServicioRepository import ServicioRepository

class ServicioService:
    def __init__(self) -> None:
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.servicio_repository = ServicioRepository(self.db)
       
    def registrar_servicio(self, codigoSer, nombre, descripcion, costo_renta, tipo_servicio):
        servicio = Servicio(codigoSer, nombre, descripcion, costo_renta, tipo_servicio)
        return self.servicio_repository.crear_servicio(servicio)

    def listar_servicio(self):
        print("Servicios: ")
        servicio = self.servicio_repository.listar_servicio()
        print("Codigo:\t Nombre:\t Descripcion:\t Costo:\t Tipo: ")
        for row in servicio:
            print(f"{row['codigoSer']}\t {row['nombre']}\t {row['descripcion']}\t {row['costoRenta']}\t")

    def listar_servicio_y_tipo(self):

        servicios = self.servicio_repository.obtener_servicios_inner()
        if servicios:
            for ser in servicios:
                print(f"Informacion de: {ser.nombre}:\n{ser.descripcion}\n{ser.costo_renta}\n{ser.tipo_nombre}")

