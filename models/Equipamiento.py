class Equipamiento:
    # Constructor 
    def __init__(self, nombre, descripcion, costoRenta, stock, tipo_equipa): 
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__costoRenta = costoRenta
        self.__stock = stock
        self.__tipo_equipa = tipo_equipa

    # Set / Get
    




    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, new_nombre):
        self.__nombre = new_nombre

    @property
    def descripcion(self):
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, new_descripcion):
        self.__descripcion = new_descripcion

    @property
    def costoRenta(self):
        return self.__costoRenta
    @costoRenta.setter
    def costoRenta(self, new_costoRenta):
        self.__costoRenta = new_costoRenta

    @property
    def stock(self):
        return self.__stock
    @stock.setter
    def stock(self, new_stock):
        self.__stock = new_stock

    @property
    def tipo_equipa(self):
        return self.__tipo_equipa
    @tipo_equipa.setter
    def tipo_equipa(self, new_tipo_equipa):
        self.__tipo_equipa = new_tipo_equipa


