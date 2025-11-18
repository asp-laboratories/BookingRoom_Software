class Rol:
    def __init__(self, codigoRol, descripcion):
        self.__codigoRol = codigoRol
        self.__descripcion = descripcion
        self.trabajadores = []

    @property
    def codigoRol(self):
        return self.__codigoRol
    @codigoRol.setter
    def codigoRol(self, codigoRol):
        self.__codigoRol = codigoRol

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion
