from repositories_crud.DatosMontajeRepository import DatosMontajeRepository
from services.TipoMontajeService import TipoMontajeService
from services.mobiliarioService import mobiliarioService
from config.db_settings import BaseDeDatos


class DatosMontajeService:
    # Constructor
    def __init__(self, db_instance):
        self.db = db_instance
        self.TipoMontajeRepository = TipoMontajeService(self.db)
        self.DatosMontajeRepository = DatosMontajeRepository(self.db)
        self.mobiliario_service = mobiliarioService(self.db)

    # Metodos
    def mobiliarios_montaje(self, tipo_montaje, datos_salon):
        numDatMon = self.TipoMontajeRepository.obtener_datos_montaje(
            tipo_montaje, datos_salon
        )

        mobiliarios = self.DatosMontajeRepository.mobiliarios_montaje(numDatMon)

        return mobiliarios

    def calcular_costo_mobiliario_montaje(self, tipo_montaje, datos_salon):
        mobiliarios = self.mobiliarios_montaje(tipo_montaje, datos_salon)
        if not mobiliarios:
            return 0.0

        total_costo = 0.0
        for mueble in mobiliarios:
            costo = self.mobiliario_service.obtener_costo_mobiliario(mueble['nombre'])
            if costo is not None:
                total_costo += costo * mueble['cantidad']
        
        return total_costo
