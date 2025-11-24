from repositories_crud.MobiliarioRepository import MobiliarioRepository
from models.Mobiliario import Mobiliario
from config.db_settings import BaseDeDatos

class mobiliarioService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.mobiliario_repository = MobiliarioRepository(self.db)

    # Metodos
    def registrar_mobiliario(self, numMob, nombre, costoRenta, stock, tipo_mob, esta_mob, trabajador):
        mobiliario = Mobiliario(numMob, nombre, costoRenta, stock, tipo_mob, esta_mob, trabajador)
        return self.mobiliario_repository.crear_mobiliario(mobiliario)
    
    def listar_mobiliarios(self): # Sin descripcion detallada de tipo, estado, trabajador
        print("Mobiliarios: ")
        mobiliarios = self.mobiliario_repository.listar_mobiliarios()

        print("Numero: \tNombre: \tCosto de Renta \tStock \t")
        for mobiliario in mobiliarios:
            print(f"{mobiliario['numMob']}\t{mobiliario['nombre']}\t{mobiliario['costoRenta']}\t{mobiliario['stock']}")
    
    def listar_mobiliarios_detallada(self): # Ya q este el modulo de tipo y estado de mobiliario, asi como caracteristicas y asi poner la descripcion detallada mas chida
        pass
