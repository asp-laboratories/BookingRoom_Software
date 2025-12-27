class caracteristicas:
    def __init__(self, mobiliario, mob_carac):
        self.__mobiliario = mobiliario
        self.__mob_carac = mob_carac

    @property
    def mobiliario(self):
        return self.__mobiliario

    @mobiliario.setter
    def mobiliario(self, mobiliario):
        self.__mobiliario = mobiliario

    @property
    def mob_carac(self):
        return self.__mob_carac

    @mob_carac.setter
        self.__mob_carac = mob_carac
