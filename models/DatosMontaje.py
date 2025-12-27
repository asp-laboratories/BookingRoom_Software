class DatosMontaje:
    def __init__(
        self,
        tipo_montaje,
        datos_salon,
        capacidad=None,
    ):
        self.__capacidad = capacidad
        self.__tipo_montaje = tipo_montaje
        self.__datos_salon = datos_salon
        self.__mobiliario = []

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, capacidad):
        self.__capacidad = capacidad

    @property
    def tipo_montaje(self):
        return self.__tipo_montaje

    @tipo_montaje.setter
    def tipo_montaje(self, tipo_montaje):
        self.__tipo_montaje = tipo_montaje

    @property
    def datos_salon(self):
        return self.__datos_salon

    @datos_salon.setter
    def datos_salon(self, datos_salon):
        self.__datos_salon = datos_salon

    @property
    def mobiliario(self):
        return self.__mobiliario

    @mobiliario.setter
    def mobiliario(self, mobiliario):
        self.__mobiliario = mobiliario
