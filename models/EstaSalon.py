class EstaSalon:
    def __init__(self, codigoSal, descripcion):
        self.__codigoSal = codigoSal
        self.__descripcion = descripcion

    @property
    def codigoSal(self):
        return self.__codigoSal

    @codigoSal.setter
    def codigoSal(self, codigoSal):
        self.__codigoSal = codigoSal

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
