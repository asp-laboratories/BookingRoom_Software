
class DatosSalon:
    # Constructor
    def __init__(self, nombre, costoRenta, ubiNombrePas, ubiNumeroPas, dimenLargo, dimenAncho, dimenAltura, mCuadrados=0, esta_salon="DISPO"):
        self.__nombre = nombre
        self.__costoRenta = costoRenta
        self.__ubiNombrePas = ubiNombrePas
        self.__ubiNumeroPas = ubiNumeroPas
        self.__dimenLargo = dimenLargo
        self.__dimenAncho = dimenAncho
        self.__dimenAltura = dimenAltura
        self.__mCuadrados = mCuadrados
        self.__esta_salon = esta_salon
    
    # Get / Set

    @property
    def costoRenta(self):
        return self.__costoRenta

    @costoRenta.setter
    def costoRenta(self, costoRenta):
        self.__costoRenta = costoRenta

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, new_nombre):
        self.__nombre = new_nombre
        
    @property
    def ubiNombrePas(self):
        return self.__ubiNombrePas
    @ubiNombrePas.setter
    def ubiNombrePas(self, new_ubiNombrePas):
        self.__ubiNombrePas = new_ubiNombrePas
        
    @property
    def ubiNumeroPas(self):
        return self.__ubiNumeroPas
    @ubiNumeroPas.setter
    def ubiNumeroPas(self, new_ubiNumeroPas):
        self.__ubiNumeroPas = new_ubiNumeroPas
        
    @property
    def dimenLargo(self):
        return self.__dimenLargo
    @dimenLargo.setter
    def dimenLargo(self, new_dimenLargo):
        self.__dimenLargo = new_dimenLargo
        
    @property
    def dimenAncho(self):
        return self.__dimenAncho
    @dimenAncho.setter
    def dimenAncho(self, new_dimenAncho):
        self.__dimenAncho = new_dimenAncho
        
    @property
    def dimenAltura(self):
        return self.__dimenAltura
    @dimenAltura.setter
    def dimenAltura(self, new_dimenAltura):
        self.__dimenAltura = new_dimenAltura
        
    @property
    def mCuadrados(self):
        return self.__mCuadrados
    @mCuadrados.setter
    def mCuadrados(self, new_mCuadrados):
        self.__mCuadrados = new_mCuadrados
        
    @property
    def esta_salon(self):
        return self.__esta_salon
    @esta_salon.setter
    def esta_salon(self, new_esta_salon):
        self.__esta_salon = new_esta_salon
    
