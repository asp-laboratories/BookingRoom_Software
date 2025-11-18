class TipoCliente:
    def __init__(self, codigoCli, descripcion):
        self.__codigoCli = codigoCli
        self.__descripcion = descripcion

    @property
    def codigoCli(self):
        return self.__codigoCli
    @codigoCli.setter
    def codigoCli(self, codigoCli):
        self.__codigoCli = codigoCli

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
