class Telefonos:
    def __init__(self, telefono, datos_cliente=None, trabajador=None):
        self.__telefono = telefono
        self.__datos_cliente = datos_cliente
        self.__trabajador = trabajador

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        self.__telefono = telefono

    @property
    def datos_cliente(self):
        return self.__datos_cliente

    @datos_cliente.setter
    def datos_cliente(self, datos_cliente):
        self.__datos_cliente = datos_cliente

    @property
    def trabajador(self):
        return self.__trabajador

    @trabajador.setter
    def trabajador(self, trabajador):
        self.__trabajador = trabajador
