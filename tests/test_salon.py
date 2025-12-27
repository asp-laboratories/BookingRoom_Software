import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.SalonServices import SalonServices

salon = SalonServices()
# salon.registrar_salones(1,"Vivaldi","pasillo rosca",3,20.5,54.4,29.4,80.4,"DISPN")


def registrar():
    while True:
        opcion = int(input("Quieres registrar un salon? 1.Si 2.No"))
        if opcion == 1:
            print("--Registro de salones--")
            nombre = input("Ingresa el nombre del salon: ")
            nombre_pasillo = input("Ingresa el nombre del pasillo en donde se ubica: ")
            numero_pasillo = int(
                input("Ingresa el numero del pasillo en donde se ubica: ")
            )
            dimeLargo = float(input("Ingresa el largo del salon: "))
            dimeAncho = float(input("Ingresa el ancho del salon: "))
            dimeAlto = float(input("Ingresa el alto del salon: "))
            m2 = 2 * (dimeLargo + dimeAncho) * dimeAlto
            print(m2)
            estado = input("Estado: ")
            salon.registrar_salones(
                nombre,
                nombre_pasillo,
                numero_pasillo,
                dimeLargo,
                dimeAncho,
                dimeAlto,
                m2,
                estado,
            )
        elif opcion == 2:
            break
        else:
            print("Intentalo de nuevo")


def listar():
    salon.listar_salones()


def asignar():
    while True:
        salon.listar_estados()
        opcion = int(input("Quieres actualizar el estado? 1. si 2. no "))
        if opcion == 1:
            numSalon = int(input("Ingresa el numero del salon: "))
            esta_salon = input("Codigo del estado: ")
            salon.actualizar_salon(numSalon, esta_salon)
            break
        elif opcion == 2:
            break
        else:
            print("Ingresa un valor correcto, porfavor")


def main():
    while True:
        print(
            "--Registro de salon--\n1. Registrar salon \n2. Listar salon\n3. Cambiar estado \n4. Salir"
        )
        opcion = int(input("Elige una opcion: "))
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
