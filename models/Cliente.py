class Cliente():
    def __init__(self, rfc, nombre, prim_apell, seg_apell, nombre_fiscal, email, fecha_nac, dir_colonia, dir_calle, dir_numero):
        self.__rfc = rfc
        self.__nombre = nombre
        self.__prim_apell = prim_apell
        self.___seg_apell = seg_apell
        self.___nombre_fiscal = nombre_fiscal
        self.___email = email
        self.___fecha_nac = fecha_nac
        self.___dir_colonia = dir_colonia
        self.__dir_calle = dir_calle
        self.__dir_numero = dir_numero

    @property
    def rfc(self):
        return self.rfc

    @rfc.setter
    def pname(self, rfc):
        self.__rfc = rfc

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def prim_apell(self):
        return self.__prim_apell

    @prim_apell.setter
    def prim_apell(self, prim_apell):
        self.__prim_apell = prim_apell

    @property
    def seg_apell(self):
        return self.__seg_apell

    @seg_apell.setter
    def seg_apell(self, seg_apell):
        self.__seg_apell = seg_apell

    @property
    def nombre_fiscal(self):
        return self.__nombre_fiscal

    @nombre_fiscal.setter
    def nombre_fiscal(self, nombre_fiscal):
        self.__nombre_fiscal = nombre_fiscal

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def fecha_nac(self):
        return self.__fecha_nac

    @fecha_nac.setter
    def fecha_nac(self, fecha_nac):
        self.__fecha_nac = fecha_nac

    @property
    def dir_colonia(self):
        return self.__dir_colonia

    @dir_colonia.setter
    def dir_colonia(self, dir_colonia):
        self.__dir_colonia = dir_colonia

    @property
    def dir_calle(self):
        return self.__dir_calle

    @dir_calle.setter
    def dir_calle(self, dir_calle):
        self.__dir_calle = dir_calle

    @property
    def dir_numero(self):
        return self.__dir_numero

    @dir_numero.setter
    def dir_numero(self, dir_numero):
        self.__dir_numero = dir_numero




















