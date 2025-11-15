class TipoServicio:
    def __init__(self, codigoTiSer, descripcion):
        self.__codigoTiSer = codigoTiSer
        self.__descripcion = descripcion
        self.__servicios = []

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

    @property
    def servicios(self):
        return self.__servicios

    @servicios.setter
    def servicios(self, servicios):
        self.__servicios = servicios

    def __str__(self):
        return (f"{self.descripcion}")
