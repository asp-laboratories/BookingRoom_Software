import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TipoServicioService import TipoServicioService
#from models.Servicios import Servicio, TipoServicio
   
def main():
    service = TipoServicioService()
    #service.registrar_tipo_servicio("SRPRN", "Servicios para reuniones")
    #service.registrar_tipo_servicio("SREJC", "Servicios ejecutivos")
    #service.registrar_tipo_servicio("SRIAV", "Acceso a internet de alta velocidad")

    #service.listar_tipos_servicio()
    service.mostrar_servicios_de_tipo("SRPRN")
if __name__ == "__main__":
    main()
