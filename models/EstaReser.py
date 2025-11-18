class EstaReser:
    def __init__(self, codigoRes, descripcion):
        self.__codigoRes = codigoRes
        self.__descripcion = descripcion

    @property
    def codigoRes(self):
        return self.__codigoRes
    @codigoRes.setter
    def codigoRes(self, codigoRes):
        self.__codigoRes = codigoRes

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
