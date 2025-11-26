from config.db_settings import BaseDeDatos
from repositories_crud.TipoMobiliarioRepository import TipoMobiliarioRepository
from models.TipoMob import TipoMob

class TipoMobiliarioService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.repository = TipoMobiliarioRepository(self.db)

    # Metodos
    def registrar_tipo_mobiliario(self, codigoTiMob, descripcion):
        if not codigoTiMob or not descripcion:
            print("Los campos no permiten nulos")
            return False
        
        tipo_equipa = TipoMob(codigoTiEquipa= codigoTiMob,descripcion= descripcion)
        return self.repository.crear_tipo_mobiliario(tipo_equipa)

    def listar_tipos_mobiliarios(self):
        print("Tipos de mobiliarios:")
        tipos_equipa = self.repository.listar_tipos_mobiliarios()
        print("Codigo: \t Descripcion:")
        for tmob in tipos_equipa:
            print(f"{tmob['codigoTiMob']}\t {tmob['descripcion']}")

    def obtener_codigo(self, descripcion):
        #print("Buscando tipo de mobiliario")
        resultado =  self.repository.codigo_tipo_mob(descripcion)
        if not resultado:
            print("No se encontro el tipo de mobiliario")
        else:
            return resultado['codigoTiMob']

    def mostra_mobiliarios_tipo(self, tipo_mob):
        pass

