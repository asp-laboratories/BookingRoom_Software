class MobCarac:
    def __init__(self, numCarac, descripcion):
        self.__numCarac = numCarac
        self.__descripcion = descripcion

    @property
    def numCarac(self):
        return self.__numCarac
    @numCarac.setter
    def numCarac(self, numCarac):
        self.__numCarac = numCarac

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
