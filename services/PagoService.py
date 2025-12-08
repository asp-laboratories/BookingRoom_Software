from config.db_settings import BaseDeDatos
from models.Pago import Pago
from repositories_crud.PagoRepository import PagoRepository
from repositories_crud.MetodoPagoRepository import MetodoPagoRepository
from repositories_crud.ConceptoPagoRepository import ConceptoPagoRepository
from services.ReservacionService import ReservacionService
from datetime import date, datetime, time

class PagoServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.PagoRepository = PagoRepository(self.db)
        self.MetodoPagoRepository = MetodoPagoRepository(self.db)
        self.ConceptoPagoRepository = ConceptoPagoRepository(self.db)
        self.RservacionService = ReservacionService()
    
    def hacer_pago(self, numReser, montoPago, descripcion, concepto, metodo):
        #concepto = self.obtener_concepto(concepto)
        #metodo = self.obtener_metodo(metodo)
        fecha = date.today()
        hora = datetime.now()
        horak = hora.strftime("%H:%M")
        print(fecha, horak)
        nopago = self.obtener_no_pago(numReser)
        if nopago >= 2:
            print("Maximo de pagos alcanzados")
            return
        else:
            if nopago ==2:
                concepto = 'LIQUI'
            saldo = self.calcular_saldo(numReser) - montoPago
            pago = Pago(montoPago, descripcion, fecha, horak, nopago + 1, saldo, numReser, metodo, concepto)
            return self.PagoRepository.crear_pago(pago)

    def listar_pagos(self):
        pago = self.PagoRepository.listar_pagos()
        return pago
    
    def actualizar_pago(self, montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo):
        return self.PagoRepository.actualizar_pago(montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo)

    def calcular_saldo(self, numReser):
        return self.PagoRepository.calcular_saldo(numReser)
    
    def eliminar_pago(self, numPago):
        return self.PagoRepository.eliminar_pago(numPago)
    
    def obtener_metodo(self, descripcion):
        resutlado = self.MetodoPagoRepository.obtener_codigo_metodo(descripcion)
        return resutlado['codigoMe']

    def obtener_concepto(self, descripcion):
        resutlado = self.ConceptoPagoRepository.obtener_codigo_concepto(descripcion)
        return resutlado['codigoConc']

    def obtener_no_pago(self, numReser):
        nopago = self.PagoRepository.obtener_no_pago(numReser)
        return nopago['pagos']
    
    def pagos_reservacion(self, numReser):
        return self.PagoRepository.pagos_reservacion(numReser)

    def recibo(self, numReser, nopago):
        return self.PagoRepository.generar_recibo(numReser, nopago)
