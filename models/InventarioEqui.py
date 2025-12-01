class InventarioEqui:
    def __init__(self,reservacion, equipamiento, cantidad):
        self.__reservacion = reservacion
        self.__equipamiento = equipamiento
        self.__cantidad = cantidad

    @property
    def reservacion(self):
        return self.__reservacion

    @reservacion.setter
    def reservacion(self, reservacion):
        self.__reservacion = reservacion

    @property
    def equipamiento(self):
        return self.__equipamiento

    @equipamiento.setter
    def equipamiento(self, equipamiento):
        self.__equipamiento = equipamiento

    @property
    def cantidad(self):
        """The cantidad property."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        self.__cantidad = cantidad
