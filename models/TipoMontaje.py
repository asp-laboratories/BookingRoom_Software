class TipoMontaje:
    def __init__(self, codigoMon, nombre, descripcion):
        self.__codigoMon = codigoMon
        self.__nombre = nombre
        self.__descripcion = descripcion

    @property
    def codigoMon(self):
        return self.__codigoMon
    @codigoMon.setter
    def codigoMon(self, codigoMon):
        self.__codigoMon = codigoMon

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
