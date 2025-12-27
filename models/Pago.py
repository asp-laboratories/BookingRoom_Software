class Pago:
    def __init__(
        self,
        montoPago,
        descripcion,
        fecha,
        hora,
        noPago,
        saldo,
        reservacion,
        metodo_pago,
        concepto_pago,
    ):
        self.__montoPago = montoPago
        self.__descripcion = descripcion
        self.__fecha = fecha
        self.__hora = hora
        self.__noPago = noPago
        self.__saldo = saldo
        self.__reservacion = reservacion
        self.__metodo_pago = metodo_pago
        self.__concepto_pago = concepto_pago

    @property
    def montoPago(self):
        return self.__montoPago

    @montoPago.setter
    def montoPago(self, montoPago):
        self.__montoPago = montoPago

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo):
        self.__saldo = saldo

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, fecha):
        self.__fecha = fecha

    @property
    def hora(self):
        return self.__hora

    @hora.setter
    def hora(self, hora):
        self.__hora = hora

    @property
    def noPago(self):
        return self.__noPago

    @noPago.setter
    def noPago(self, noPago):
        self.__noPago = noPago

    @property
    def reservacion(self):
        return self.__reservacion

    @reservacion.setter
    def reservacion(self, reservacion):
        self.__reservacion = reservacion

    @property
    def metodo_pago(self):
        return self.__metodo_pago

    @metodo_pago.setter
    def metodo_pago(self, metodo_pago):
        self.__metodo_pago = metodo_pago

    @property
    def concepto_pago(self):
        return self.__concepto_pago

    @concepto_pago.setter
    def concepto_pago(self, concepto_pago):
        self.__concepto_pago = concepto_pago
