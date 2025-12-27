class Trabajador:
    def __init__(
        self,
        rfc,
        numTrabajador,
        nombre,
        priApellido,
        segApellido,
        email,
        codigoRol="DEFLT",
        rolObj=None,
    ):
        self.__rfc = rfc
        self.__numTrabajador = numTrabajador
        self.__nombre = nombre
        self.__priApellido = priApellido
        self.__segApellido = segApellido
        self.__numTrabajador = numTrabajador
        self.__email = email
        self.__codigoRol = codigoRol
        self.rolObj = rolObj

    @property
    def rfc(self):
        return self.__rfc

    @rfc.setter
    def rfc(self, rfc):
        self.__rfc = rfc

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def numTrabajador(self):
        return self.__numTrabajador

    @numTrabajador.setter
    def numTrabajador(self, numTrabajador):
        self.__numTrabajador = numTrabajador

    @property
    def priApellido(self):
        return self.__priApellido

    @priApellido.setter
    def priApellido(self, priApellido):
        self.__priApellido = priApellido

    @property
    def segApellido(self):
        return self.__segApellido

    @segApellido.setter
    def segApellido(self, segApellido):
        self.__segApellido = segApellido

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def codigoRol(self):
        return self.__codigoRol

    @codigoRol.setter
    def codigoRol(self, codigoRol):
        self.__codigoRol = codigoRol

    def __str__(self):
        return f"--INFORMACION DEL TRABAJADOR-- RFC: {self.rfc}, Nombre completo: {self.nombre} {self.priApellido} {self.segApellido}"
