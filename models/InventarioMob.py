
class InventarioMob:
    # Constructor
    def __init__(self, esta_mob, cantidad, mobiliario = None):
        self.__esta_mob = esta_mob        
        self.__cantidad = cantidad   
        self.__mobiliario = mobiliario

    # Metodos
    @property
    def esta_mob(self):
        return self.__esta_mob
    @esta_mob.setter
    def esta_mob(self, new_esta_mob):
        self.__esta_mob = new_esta_mob

    @property
    def cantidad(self):
        return self.__cantidad
    @cantidad.setter
    def cantidad(self, new_cantidad):
        self.__cantidad = new_cantidad

    @property
    def mobiliario(self):
        return self.__mobiliario
    @mobiliario.setter
    def mobiliario(self, new_mobiliario):
        self.__mobiliario = new_mobiliario

    def __str__(self):
        return self.esta_mob
