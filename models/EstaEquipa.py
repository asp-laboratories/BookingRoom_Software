class EstaEquipa:
    def __init__(self, codigoEquipa, descripcion):
        self.__codigoEquipa = codigoEquipa
        self.__descripcion = descripcion

    @property
    def codigoEquipa(self):
        return self.__codigoEquipa

    @codigoEquipa.setter
    def codigoMe(self, codigoEquipa):
        self.__codigoEquipa = codigoEquipa

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
