class ReserEquipamiento:
    # Constructor
    def __init__(self, equipamiento, cantidad, reservacion=None):
        self.__equipamiento = equipamiento
        self.__cantidad = cantidad
        self.__reservacion = reservacion

    # Metodos
    @property
    def equipamiento(self):
        return self.__equipamiento

    @equipamiento.setter
    def equipamiento(self, new_equipamiento):
        self.__equipamiento = new_equipamiento

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, new_cantidad):
        self.__cantidad = new_cantidad

    @property
    def reservacion(self):
        return self.__reservacion

    @reservacion.setter
    def reservacion(self, new_reservacion):
        self.__reservacion = new_reservacion
