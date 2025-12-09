import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.RolService import RolService

def main():
    rol_services = RolService()
    # rol_services.registrar_rol("DEFLT","Predeterminado")
    print(rol_services.listar_rol())

    #trabas = rol_services.obtener_trabajadores_rol('Predeterminado')

    #for i in trabas:
    #    print(f"{i['nombre']} y {i['telefonos']}\n")

main()
