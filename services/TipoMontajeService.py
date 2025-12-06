from config.db_settings import BaseDeDatos
from models.DatosMontaje import DatosMontaje
from repositories_crud.TipoMontajeRepository import TipoMontajeRepository
from repositories_crud.DatosMontajeRepository import DatosMontajeRepository
from services.SalonServices import SalonServices
from models.MontajeMobiliario import MontajeMobilario

class TipoMontajeService:
    # Constructor
    def __init__(self):
        db = BaseDeDatos(database='BookingRoomLocal')
        # db = BaseDeDatos(database='BookingRoomLoca')
        self.TipoMontajeRepository = TipoMontajeRepository(db)
        self.DatosMontajeRepository = DatosMontajeRepository(db)
        self.SalonServices = SalonServices()

    # Metodos
    def listar_tipos_montajes(self):
        tipos_montajes = self.TipoMontajeRepository.listar_tipos_montajes()
        return tipos_montajes
    
    def listar_mobiliarios_montaje(self, montaje):
        montaje = self.TipoMontajeRepository.obtener_codigo_montaje(montaje) 
        resultado = self.TipoMontajeRepository.mobiliarios_por_montaje(montaje['codigoMon'])
        salonesMobiliarios = [] # Dentro de esto van los diccionarios con la info
        nombresSalones = []
        for registro in resultado: # Se recorre el reusltado de la consulta
            if registro['salon'] not in nombresSalones:
                nombresSalones.append(registro['salon'])
        
        for nombreSalon in nombresSalones:
            salon = {
                'nombre'     : nombreSalon,
                'mobiliarios': []
                    }
            
            for reg in resultado:
                if reg['salon'] == nombreSalon:
                    mobiliario = MontajeMobilario(reg['mobiliario'], reg['cantidad'])
                    salon['mobiliarios'].append(mobiliario)

            salonesMobiliarios.append(salon)
                    
            
        return salonesMobiliarios

    def registrar_datos_montaje(self, cantidad, tipos_montaje, datos_salon):
        datos = DatosMontaje(cantidad, tipos_montaje, datos_salon)
        return self.TipoMontajeRepository.ingresar_datos_montaje(datos)
    
    def obtener_datos_montaje(self, tipo_montaje, datos_salon):
        datos_salon = self.SalonServices.obtener_codigo_salon(datos_salon)
        tipo_montaje = self.TipoMontajeRepository.obtener_codigo_montaje(tipo_montaje)
        datos_montaje = DatosMontaje(tipo_montaje=tipo_montaje['codigoMon'], datos_salon=datos_salon)
        numDatMon =  self.DatosMontajeRepository.obtener_codigo_datos_montaje(datos_montaje)
        return numDatMon['numDatMon']
