class EstaMob:
    def __init__(self, codigoMob, descripcion):
        self.__codigoMob = codigoMob
        self.__descripcion = descripcion

    @property
    def codigoMob(self):
        return self.__codigoMob

    @codigoMob.setter
    def codigoMob(self, codigoMob):
        self.__codigoMob = codigoMob

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    def __str__(self):
        return self.descripcion
