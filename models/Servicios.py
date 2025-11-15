class Servicio:
    def __init__(self, codigoSer, nombre, descripcion, costo_renta, tipo_servicio, tipo=None):
        self.__codigoSer = codigoSer
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__costo_renta = costo_renta
        self.__tipo_servicio = tipo_servicio
        self.tipo = tipo

    @property
    def codigoSer(self):
        return self.__codigoSer

    @codigoSer.setter
    def codigoSer(self, codigoSer):
        self.__codigoSer = codigoSer

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def costo_renta(self):
        return self.__costo_renta

    @costo_renta.setter
    def costo_renta(self, costo_renta):
        self.__costo_renta = costo_renta

    @property
    def tipo_servicio(self):
        return self.__tipo_servicio

    @tipo_servicio.setter
    def tipo_servicio(self, tipo_servicio):
        self.__tipo_servicio = tipo_servicio


        
        
