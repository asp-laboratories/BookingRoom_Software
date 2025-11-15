import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ServicioServices import ServicioService
   
def main():

    servicio_service = ServicioService()
    eleccion_panel = int(input("--Panel servicio--\n1. Registrar servicio\n2. Listar servicios\nOpcion: "))
    if eleccion_panel == 1:
        servicio_service.registrar_servicio("SRVDC","Servicio de copiado", "Copias", 20.00, "SRPRN")
    elif eleccion_panel == 2:
        servicio_service.listar_servicio()
    else:
        print("No existe esa opcion")
if __name__ == "__main__":
    main()
