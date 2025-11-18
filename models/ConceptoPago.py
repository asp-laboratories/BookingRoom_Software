class ConceptoPago:
    def __init__(self, codigoConc, descripcion):
        self.__codigoConc = codigoConc
        self.__descripcion = descripcion

    @property
    def codigoConc(self):
        return self.__codigoConc
    @codigoConc.setter
    def codigoMe(self, codigoConc):
        self.__codigoConc = codigoConc

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
