import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TrabajadorServices import TrabajadorServices


trabajador = TrabajadorServices()
def registrar():
    while True:
        opcion = int(input("Quieres registrar un trabajador? 1.Si 2.No"))
        if opcion == 1:
            print("--Registro de trabajadores--")
            rfc = input("Ingresa tu RFC: ")
            numero_emple = input("Ingresa tu numero de empleado: ")
            nombre = input("Ingresa tu nombre: ")
            apellido_paterno = input("Ingresa tu apellido paterno: ")
            apellido_materno = input("Ingresa tu apellido materno: ")
            email = input("Ingresa tu correo electronico: ")
            trabajador.registrar_trabajadores(rfc,numero_emple,nombre,apellido_paterno,apellido_materno,email)
        elif opcion == 2:
            break
        else:
            print("Ingrese una opcion correcta")
            
def asignar():
    while True:
        opcion = int(input("Quieres actualizar el rol? 1. si 2. no "))
        if opcion == 1:
            RFC = input("RFC: ")
            codigoRol = input("codigoRol: ")
            trabajador.actualizar_trabajadores(RFC, codigoRol)
            break
        elif opcion == 2:
            break
        else:
            print("Ingresa un valor correcto, porfavor")

def listar():
    trabajador.listar_trabajadores()



def main():
    while True:
        print("--Registro de trabajador--\n1. Registrar trabajador \n2. Listar trabajador\n 3. Asignar rol \n4. Salir")
        opcion = int(input("Elige una opcion"))
        if opcion == 1:
            registrar()
        if opcion == 2:
            listar()
        elif opcion == 3:
            asignar()
        elif opcion == 4:
            break
        else:
            print("Ingresa un opcion correcta: ")



if __name__ == "__main__":
    main()
