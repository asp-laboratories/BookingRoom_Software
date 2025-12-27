import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_salon import main as main_salones
from tests.test_servicio import main as main_servicios
from tests.test_tipo_servicio import main as main_tipoServicios
from tests.test_trabajador import asignar as establecer_rol, listar
from utils.Obtener_Numeros import obt_int
from tests.test_equipamento import main as main_equipamiento
from tests.test_tipoEquipamento import main as main_tiEquipamento


def menu_administrador():
    while True:
        print("\nQue deseas hacer?")
        respuesta = obt_int(
            "\n1. Salon \n2. Equipamento \n3. Servicio \n4. Mobiliario \n5. Asignar rol\n6. Listar trabajadores \n0. Salir"
        )
        match respuesta:
            case 0:
                print("Saliendo...")
                break

            case 1:
                print("Menu salones")
                main_salones()

            case 2:
                print("Menu equipamento")
                print("A que menu desea ingresar?")
                while True:
                    respuesta = obt_int(
                        "1. Menu Tipo de Equipamento \n2. Menu Equipamentos \n0. Salir"
                    )
                    match respuesta:
                        case 0:
                            print("Saliendo...")
                            break
                        case 1:
                            main_tiEquipamento()

                        case 2:
                            main_equipamiento()

                        case _:
                            print("Valor fuera de rango, intente de nuevo")

            case 3:
                print("Menu servicio")
                while True:
                    print("A que menu desea ingresar?")
                    respuesta = obt_int(
                        "1. Menu Tipo de servicio \n2. Menu Servicios \n0. Salir"
                    )
                    if respuesta == 0:
                        print("Saliendo")
                        break
                    elif respuesta == 1:
                        main_tipoServicios()
                    elif respuesta == 2:
                        main_servicios()
                    else:
                        print("Valor fuera de rango, intentar de nuevo")

            case 4:
                print("Menu mobiliario")
                print("En proceso")
            case 5:
                print("Menu trabajadores")
                establecer_rol()

            case 6:
                print("Lista de los trabajadores")
                listar()

            case _:
                print("Valor fuera de rango intente de nuevo")


if __name__ == "__main__":
    menu_administrador()
