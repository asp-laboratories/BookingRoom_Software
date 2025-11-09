class Trabajador:
    def __init__(self, rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email):
        self.__rfc = rfc
        self.__nombre = nombre
        self.__prim_apell = prim_apell
        self.__seg_apell = seg_apell
        self.__matricula = matricula
        self.__numero_emple = numero_emple
        self.__telefono = telefono
        self.__email = email

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
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, matricula):
        self.__matricula = matricula

    @property
    def numero_emple(self):
        return self.__numero_emple

    @numero_emple.setter
    def numero_emple(self, numero_emple):
        self.__numero_emple = numero_emple

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        self.__telefono = telefono

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    def __str__(self):
        return f"--INFORMACION DEL TRABAJADOR-- RFC: {self.rfc}, Nombre completo: {self.nombre} {self.prim_apell} {self.seg_apell}"



class Administrador(Trabajador):
    def __init__(self,rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email):
        super().__init__(rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email)
    
    def asignar_roles(self):
        pass

    def eliminar_roles(self):
        pass

    def añadir_equipamiento(self):
        pass

    def eliminar_equipamiento(self):
        pass

    def actualizar_equipamiento(self):
        pass

    def añadir_servicio(self):
        pass
    
    def eliminar_servicio(self):
        pass

    def actualizar_servicio(self):
        pass


class Recepcionista(Trabajador):
    def __init__(self,rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email):
        super().__init__(rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email)


class Almacenista(Trabajador):
    def __init__(self,rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email):
        super().__init__(rfc, nombre, prim_apell, seg_apell, matricula, numero_emple, telefono, email)

    def cambiar_estado_mob(self):
        pass

def main():
    t1 = Trabajador("1234567890123", "Jacinto", "Zamorano", "Perez", 62471,18,6632832828,"jacinto@gmail.com")
    print(t1)

# Bloque de ejecución principal, ahora debajo de la definición de main()
if __name__ == "__main__":
    main()
