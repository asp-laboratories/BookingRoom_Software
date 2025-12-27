from config.db_settings import BaseDeDatos
from models.TipoServicio import TipoServicio
from repositories_crud.TipoServiciosRepository import TipoServiciosRepository


class TipoServicioService:
    def __init__(self):
        self.db = BaseDeDatos(database="BookingRoomLocal")
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.repository = TipoServiciosRepository(self.db)

    def registrar_tipo_servicio(self, codigoTiSer, descripcion):
        if not codigoTiSer or not descripcion:
            print("Los campos no permiten nulos")
            return False

        tipo_servicio = TipoServicio(codigoTiSer=codigoTiSer, descripcion=descripcion)
        return self.repository.crear_tipo_servicio(tipo_servicio)

    def listar_tipos_servicio(self, descripcion):  # PAra un tiop de servicio
        return self.repository.listar_tipo_servicio(descripcion)

    def listar_tipos_servicios(self):  # Pa muchos tipos de servicios
        return self.repository.listar_tipos_sevicios()

    def mostrar_servicios_de_tipo(self, tipo_servicio):
        codigoTS = self.repository.obtener_codigo_tipo(tipo_servicio)
        return self.repository.obtener_servicios_de_tipo(codigoTS["codigoTiSer"])
        #
        # if tipo:
        #     print(f"\n--- {tipo} ---")
        #     print("Servicios:")
        #     if tipo.servicios:
        #         for servicios in tipo.servicios:
        #             print(f"  - {servicios.nombre}")
        #     else:
        #         print(" No tiene servicios registrados")
        # else:
        #     print("Tipo de servicio no encontrado, revise el codigo")
