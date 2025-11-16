from config.db_settings import BaseDeDatos
from models.TipoServicio import TipoServicio
from repositories_crud.TipoServiciosRepository import TipoServiciosRepository


class TipoServicioService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.repository = TipoServiciosRepository(self.db)

    def registrar_tipo_servicio(self, codigoTiSer, descripcion):
        if not codigoTiSer or not descripcion:
            print("Los campos no permiten nulos")
            return False

        tipo_servicio = TipoServicio(codigoTiSer=codigoTiSer,descripcion=descripcion)
        return self.repository.crear_tipo_servicio(tipo_servicio)

    def listar_tipos_servicio(self):
        print("Tipos de servicios: ")
        tipo_servicio = self.repository.listar_tipo_servicio()
        print("Codigo:\t Descripcion:")
        for row in tipo_servicio:
            print(f"{row['codigoTiSer']}\t {row['descripcion']}")
    
    def mostrar_servicios_de_tipo(self, tipo_servicio):
        tipo = self.repository.obtener_servicios_de_tipo(tipo_servicio)
        
        if tipo:
            print(f"\n--- {tipo} ---")
            print("Servicios:")
            if tipo.servicios:
                for servicios in tipo.servicios:
                    print(f"  - {servicios.nombre}")
            else:
                print(" No tiene servicios registrados")
        else:
            print("Tipo de servicio no encontrado, revise el codigo")
        


