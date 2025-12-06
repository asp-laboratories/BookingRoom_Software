
class MontajeMobilario:
    # Constructor
    def __init__(self, mobiliario, cantidad):
        self.__mobiliario = mobiliario
        self.__cantidad = cantidad
    
    # Get / Set
    @property
    def mobiliario(self):
        return self.__mobiliario
    @mobiliario.setter
    def mobiliario(self, new_mobiliario):
        self.__mobiliario = new_mobiliario    

    @property
    def cantidad(self):
        return self.__cantidad
    @cantidad.setter
    def cantidad(self, new_cantidad):
        self.__cantidad = new_cantidad