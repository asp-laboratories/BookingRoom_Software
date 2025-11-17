class Permiso:
    def __init__(self, codigoPer, descripcion):
        self.__codigoPer = codigoPer
        self.__descripcion = descripcion

    @property
    def codigoPer(self):
        return self.__codigoPer

    @codigoPer.setter
    def codigoPer(self, codigoPer):
        self.__codigoPer = codigoPer

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
