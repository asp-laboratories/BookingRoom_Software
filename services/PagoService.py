from config.db_settings import BaseDeDatos
from models.Pago import Pago
from repositories_crud.PagoRepository import PagoRepository

class PagoServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.PagoRepository = PagoRepository(self.db)
    
    def listar_pagos(self):
        pago = self.PagoRepository.listar_pagos()
        return pago
    
    def actualizar_pago(self, montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo):
        return self.PagoRepository.actualizar_pago(montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo)

    def calcular_saldo(self, numReser):
        return self.PagoRepository.calcular_saldo(numReser)