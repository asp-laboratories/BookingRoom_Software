import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.DatosClienteService import DatosClienteServices

cliente = DatosClienteServices()
def registrar():
    while True:
        opcion = int(input("Quieres registrar un cliente? 1.Si 2.No"))
        if opcion == 1:
            print("--Registro de clientes--")
            rfc = input("Ingresa tu RFC: ")
            nombre = input("Ingresa tu nombre: ")
            apellido_paterno = input("Ingresa tu apellido paterno: ")
            apellido_materno = input("Ingresa tu apellido materno: ")
            nombre_fiscal = input("Ingresa tu apellido materno: ")
            email = input("Ingresa tu correo electronico: ")
            print("Direccion")
            calle = input("Calle: ")
            colonia = input("Colonia: ")
            numero = input("Numero: ")
            tipo_cliente = input("Tipo: ")
            cliente.registrar_clientes(rfc,nombre,apellido_paterno, apellido_materno, nombre_fiscal, email, calle, colonia, numero, tipo_cliente)
        elif opcion == 2:
            break
        else:
            print("Ingrese una opcion correcta")
            
# def asignar():
#     while True:
#         opcion = int(input("Quieres actualizar el rol? 1. si 2. no "))
#         if opcion == 1:
#             RFC = input("RFC: ")
#             codigoRol = input("codigoRol: ")
#             cliente.actualizar_cliente(RFC, codigoRol)
#             break
#         elif opcion == 2:
#             break
        # else:
        #     print("Ingresa un valor correcto, porfavor")

def listar():
    cliente.listar_clientes()



def main():
    while True:
        print("--Registro de cliente--\n1. Registrar cliente \n2. Listar clientes \n3. Salir")
        opcion = int(input("Elige una opcion"))
        if opcion == 1:
            registrar()
        if opcion == 2:
            listar()
        elif opcion == 3:
            break
        else:
            print("Ingresa un opcion correcta: ")



if __name__ == "__main__":
    main()
