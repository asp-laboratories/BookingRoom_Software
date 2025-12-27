class TipoMob:
    def __init__(self, codigoTiMob, descripcion):
        self.__codigoTiMob = codigoTiMob
        self.__descripcion = descripcion
        self.__mobiliarios = []

    @property
    def codigoTiMob(self):
        return self.__codigoTiMob

    @codigoTiMob.setter
    def codigoTiMob(self, codigoTiMob):
        self.__codigoTiMob = codigoTiMob

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def mobiliarios(self):
        return self.__mobiliarios

    @mobiliarios.setter
    def mobiliarios(self, new_mobiliarios):
        self.__mobiliarios = new_mobiliarios

    def __str__(self):
        return self.descripcion
