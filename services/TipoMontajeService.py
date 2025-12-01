from config.db_settings import BaseDeDatos
from models.DatosMontaje import DatosMontaje
from repositories_crud.TipoMontajeRepository import TipoMontajeRepository

class TipoMontajeService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database='BookingRoomLocal')
        self.TipoMontajeRepository = TipoMontajeRepository(db)

    # Metodos
    def listar_tipos_montajes(self):
        tipos_montajes = self.TipoMontajeRepository.listar_tipos_montajes()
        return tipos_montajes
    
    def listar_mobiliarios_montaje(self, montaje):
        montaje = self.TipoMontajeRepository.obtener_codigo_montaje(montaje) 
        resultado = self.TipoMontajeRepository.mobiliarios_por_montaje(montaje['codigoMon'])
        print(resultado)

    def registrar_datos_montaje(self, cantidad, tipos_montaje, datos_salon):
        datos = DatosMontaje(cantidad, tipos_montaje, datos_salon)
        return self.TipoMontajeRepository.ingresar_datos_montaje(datos)
