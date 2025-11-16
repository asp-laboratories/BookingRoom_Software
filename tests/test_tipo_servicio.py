import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TipoServicioService import TipoServicioService
service = TipoServicioService()


def registrar_tipo():
    while True:
        opcion = int(input("\n¿Agregar tipo de servicio?\n1. Si\n2. No\nopcion: "))
        if opcion == 1:
            codigo = input("Codigo de tipo:")
            descripcion = input("Descripcion del tipo: ")
            service.registrar_tipo_servicio(codigo, descripcion)
        elif opcion == 2:
            break
        else:
            print("Escribe una opcion correcta")

def mostrar_tipo_con_ser():
    while True:
        opcion = int(input("\nMostrar los servicios de un tipo de servicio:\n1. Si \n2. No\nopcion: "))
        if opcion == 1:
            codigoTiSer = input("Codigo del tipo: ")
            service.mostrar_servicios_de_tipo(codigoTiSer)
        elif opcion == 2:
            break 
        else:
            print("Vuelve a ingresar")
def main():
    while True:
        opcion = int(input("\n--panel tipo de servicios--\n1.Agregar. \n2.Listar\n3.Listar un tipo con sus servicios\n4.Salir\n opcion: "))
        if opcion == 1:
            registrar_tipo()
        elif opcion == 2:
            service.listar_tipos_servicio()
        elif opcion == 3:
            mostrar_tipo_con_ser()
        elif opcion == 4:
            break
        else:
            print("No existe esa opcion ingresa de nuevo")
            
if __name__ == "__main__":
    main()
