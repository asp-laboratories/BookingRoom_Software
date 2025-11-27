class MobCarac:
    def __init__(self, nombreCarac, tipo_carac):
        self.__nombreCarac = nombreCarac
        self.__tipo_carac = tipo_carac

    @property
    def nombreCarac(self):
        return self.__nombreCarac
    @nombreCarac.setter
    def nombreCarac(self, nombreCarac):
        self.__nombreCarac = nombreCarac

    @property
    def tipo_carac(self):
        return self.__tipo_carac
    @tipo_carac.setter
    def tipo_carac(self, tipo_carac):
        self.__tipo_carac = tipo_carac

    def __str__(self):
        return self.nombreCarac