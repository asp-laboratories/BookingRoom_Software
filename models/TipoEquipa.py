class TipoEquipa:
    def __init__(self, codigoTiEquipa, descripcion):
        self.__codigoTiEquipa = codigoTiEquipa
        self.__descripcion = descripcion

    @property
    def codigoTiEquipa(self):
        return self.__codigoTiEquipa
    @codigoTiEquipa.setter
    def codigoTiEquipa(self, codigoTiEquipa):
        self.__codigoTiEquipa = codigoTiEquipa

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion


