class Rol:
    def __init__(self, codigoRol, nombre):
        self.__codigoRol = codigoRol
        self.__nombre = nombre

    @property
    def codigoRol(self):
        return self.__codigoRol

    @codigoRol.setter
    def codigoRol(self, codigoRol):
        self.__codigoRol = codigoRol

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre
