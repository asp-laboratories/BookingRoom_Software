
class DatosCliente:
    # Constructor
    def __init__(self, RFC, contNombre, contPriApellido, contSegApellido, nombreFiscal, email, dirCalle, dirColonia, dirNumero, tipo_cliente):
        self.__RFC = RFC
        self.__contNombre = contNombre
        self.__contPriApellido = contPriApellido
        self.__contSegApellido = contSegApellido
        self.__nombreFiscal = nombreFiscal
        self.__email = email
        self.__dirCalle = dirCalle
        self.__dirColonia = dirColonia
        self.__dirNumero = dirNumero
        self.__tipo_cliente = tipo_cliente

    # Set / Get
    @property
    def RFC(self):
        return self.__RFC
    @RFC.setter
    def RFC(self, new_RFC):
        self.__RFC = new_RFC

    @property
    def contNombre(self):
        return self.__contNombre
    @contNombre.setter
    def contNombre(self, new_contNombre):
        self.__contNombre = new_contNombre

    @property
    def contPriApellido(self):
        return self.__contPriApellido
    @contPriApellido.setter
    def contPriApellido(self, new_contPriApellido):
        self.__contPriApellido = new_contPriApellido

    @property
    def contSegApellido(self):
        return self.__contSegApellido
    @contSegApellido.setter
    def contSegApellido(self, new_contSegApellido):
        self.__contSegApellido = new_contSegApellido

    @property
    def nombreFiscal(self):
        return self.__nombreFiscal
    @nombreFiscal.setter
    def nombreFiscal(self, new_nombreFiscal):
        self.__nombreFiscal = new_nombreFiscal

    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, new_email):
        self.__email = new_email

    @property
    def dirCalle(self):
        return self.__dirCalle
    @dirCalle.setter
    def dirCalle(self, new_dirCalle):
        self.__dirCalle = new_dirCalle

    @property
    def dirColonia(self):
        return self.__dirColonia
    @dirColonia.setter
    def dirColonia(self, new_dirColonia):
        self.__dirColonia = new_dirColonia

    @property
    def dirNumero(self):
        return self.__dirNumero
    @dirNumero.setter
    def dirNumero(self, new_dirNumero):
        self.__dirNumero = new_dirNumero

    @property
    def tipo_cliente(self):
        return self.__tipo_cliente
    @tipo_cliente.setter
    def tipo_cliente(self, new_tipo_cliente):
        self.__tipo_cliente = new_tipo_cliente

