class TipoCarac:
    def __init__(self, codigoTiCarac, nombreCarac):
        self.__codigoTiCarac = codigoTiCarac
        self.__nombreCarac = nombreCarac

    @property
    def codigoTiCarac(self):
        return self.__codigoTiCarac

    @codigoTiCarac.setter
    def codigoTiCarac(self, codigoTiCarac):
        self.__codigoTiCarac = codigoTiCarac

    @property
    def nombreCarac(self):
        return self.__nombreCarac

    @nombreCarac.setter
    def nombreCarac(self, nombreCarac):
        self.__nombreCarac = nombreCarac

    def __str__(self):
        return self.nombreCarac
