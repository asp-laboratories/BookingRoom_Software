
class TipoMontaje:
    # Constructor
    def __init__(self, codigoMon, nombre, descripcion):
        self.__codigoMon = codigoMon
        self.__nombre = nombre
        self.__descripcion = descripcion

    # Set / Get
    @property
    def codigoMon(self):
        return self.__codigoMon
    @codigoMon.setter
    def codigoMon(self, new_codigoMon):
        self.__codigoMon = new_codigoMon

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, new_nombre):
        self.__nombre = new_nombre

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, new_descripcion):
        self.__descripcion = new_descripcion
