class MetodoPago:
    def __init__(self, codigoMe, descripcion):
        self.__codigoMe = codigoMe
        self.__descripcion = descripcion

    @property
    def codigoMe(self):
        return self.__codigoMe

    @codigoMe.setter
    def codigoMe(self, codigoMe):
        self.__codigoMe = codigoMe

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
