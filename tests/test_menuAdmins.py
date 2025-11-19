
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from config.db_settings import BaseDeDatos
from tests.test_salon import main as  main_salones
from tests.test_servicio import main as main_servicios
from tests.test_tipo_servicio import main as main_tipoServicios
from tests.test_trabajador import main as main_trabajador
from utils.Obtener_Numeros import obt_int 

def menu_administrador():
    print("Que deseas hacer?")
    while True:
        respuesta = obt_int("1. Salon \n2. Equipamento \n3. Servicio \n4. Mobiliario \n5. Trabajadores \n0. Salir")
        match respuesta:
            case 0:
                print("Saliendo...")
                break

            case 1:
                print("Menu salones")
                main_salones()
        
            case 2:
                print("Menu equipamento")
                

            case 3:
                print("Menu servicio")
                while True:
                    print("A que menu desea ingresar?")
                    respuesta = obt_int("1. Menu Tipo de servicio \n2. Servicios \n0. Salir")
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
                

            case 5:
                print("Menu trabajadores")
                main_trabajador()

            case _:
                print("Valor fuera de rango intente de nuevo")

if __name__ == "__main__":
    bd = BaseDeDatos(database="bookingroomlocal")
    menu_administrador()