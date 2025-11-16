import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.RolService import RolService

def main():
    rol_services = RolService()
    # rol_services.registrar_rol("DEFLT","Predeterminado")
    rol_services.listar_rol()
main()
