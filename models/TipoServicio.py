class TipoServicio:
    def __init__(self, codigoTiSer, descripcion):
        self.__codigoTiSer = codigoTiSer
        self.__descripcion = descripcion

    @property
    def codigoTiSer(self):
        return self.__codigoTiSer

    @codigoTiSer.setter
    def codigoTiSer(self, codigoTiSer):
        self.__codigoTiSer = codigoTiSer
        
    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion


