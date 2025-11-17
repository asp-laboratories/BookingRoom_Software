import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ServicioServices import ServicioService

servicio_service = ServicioService()
def añadir_ser():
    while True:
        ciclo = int(input("¿Añadir servicio?\n1. Si \n2. No\nOpcion: "))
        if ciclo == 1:
            codigo = input("Codigo de servicio: ")
            nombre = input("Nombre del servicio: ")
            descripcion = input("descripcion del servicio: ")
            costo = float(input("Costo del servicio: "))
            tipo = input("Codigo del tipo de servicio")
            servicio_service.registrar_servicio(codigo,nombre, descripcion, costo, tipo)
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
        eleccion_panel = int(input("--Panel servicio--\n1. Registrar servicio\n2. Listar servicios\n3. Salir \nOpcion: "))
        if eleccion_panel == 1:
            añadir_ser()
        elif eleccion_panel == 2:
            listar_ser()
        elif eleccion_panel == 3:
            break
        else:
            print("No existe esa opcion")


if __name__ == "__main__":
    main()



