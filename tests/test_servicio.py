import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ServicioServices import ServicioService

servicio_service = ServicioService()


def añadir_ser():
    while True:
        ciclo = int(input("¿Añadir servicio?\n1. Si \n2. No\nOpcion: "))
        if ciclo == 1:
            nombre = input("Nombre del servicio: ")
            descripcions = input("descripcion del servicio: ")
            costo = float(input("Costo del servicio: "))
            descripcion = input("Descripcion: ")
            servicio_service.registrar_servicio(
                nombre, descripcions, costo, descripcion
            )
        elif ciclo == 2:
            break
        else:
            print("Esa opcion no existe, ingrese una opcion valida")


def actualizar_ser():
    while True:
        ciclo = int(input("¿Actualizar servicio?\n1. Si \n2. No\nOpcion: "))
        if ciclo == 1:
            campo = input(
                "\nnombre\ndescripcion\ncostoRenta\ntipo_servicio\nNombre del campo: "
            )
            numServicio = input("Ingrese el numero del servicio: ")
            nuevoValor = input("Nuevo valor: ")
            servicio_service.actualizar_campos(campo, numServicio, nuevoValor)
        elif ciclo == 2:
            break
        else:
            print("Esa opcion no existe, ingrese una opcion valida")


def eliminar():
    while True:
        ciclo = int(input("¿Eliminar servicio?\n1. Si \n2. No\nOpcion: "))
        if ciclo == 1:
            numServicio = input("Ingrese el numero del servicio: ")
            servicio_service.eliminar_fila(numServicio)
        elif ciclo == 2:
            break
        else:
            print("Esa opcion no existe, ingrese una opcion valida")


def listar_ser():
    while True:
        servicio_service.listar_servicio_y_tipo()
        break


def main():
    while True:
        eleccion_panel = int(
            input(
                "--Panel servicio--\n1. Registrar servicio\n2. Listar servicios\n3. Actualizar \n4. Eliminar \n5. Salir \nOpcion: "
            )
        )
        if eleccion_panel == 1:
            añadir_ser()
        elif eleccion_panel == 2:
            listar_ser()
        elif eleccion_panel == 3:
            actualizar_ser()
        elif eleccion_panel == 4:
            eliminar()
        elif eleccion_panel == 5:
            break
        else:
            print("No existe esa opcion")


if __name__ == "__main__":
    main()
