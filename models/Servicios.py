class Servicio:
    def __init__(self, codigo, nombre, costo_renta, tipo_servicio):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__costo_renta = costo_renta
        self.__tipo_servicio = tipo_servicio

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def tipo_servicio(self):
        return self.__tipo_servicio

    @tipo_servicio.setter
    def tipo_servicio(self, tipo_servicio):
        self.__tipo_servicio = tipo_servicio


        
        
