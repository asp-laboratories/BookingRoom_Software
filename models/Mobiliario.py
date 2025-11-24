
class Mobiliario:
    # Constructor 
    def __init__(self, numMob, nombre, costoRenta, stock, esta_mob, tipo_mob, trabajador = None):
      self.__numMob = numMob        
      self.__nombre = nombre
      self.__costoRenta = costoRenta
      self.__stock = stock
      self.__esta_mob = esta_mob
      self.__tipo_mob = tipo_mob
      self.__trabajador = trabajador

    # Metodos
    @property
    def numMob(self):
      return self.__numMob
    @numMob.setter
    def numMob(self, new_numMob):
      self.__numMob = new_numMob
    
    @property
    def nombre(self):
      return self.__nombre
    @nombre.setter
    def nombre(self, new_nombre):
      self.__nombre = new_nombre
    
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
    def esta_mob(self):
      return self.__esta_mob
    @esta_mob.setter
    def esta_mob(self, new_esta_mob):
      self.__esta_mob = new_esta_mob
    
    @property
    def tipo_mob(self):
      return self.__tipo_mob
    @tipo_mob.setter
    def tipo_mob(self, new_tipo_mob):
      self.__tipo_mob = new_tipo_mob
    
    @property
    def trabajador(self):
      return self.__trabajador
    @trabajador.setter
    def trabajador(self, new_trabajador):
      self.__trabajador = new_trabajador
    