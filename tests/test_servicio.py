import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TipoServicioService import TipoServicioService
#from models.Servicios import Servicio, TipoServicio
   
def main():
    service = TipoServicioService()
    #service.registrar_tipo_servicio("SEML", "Empresarial")
    
    service.listar_tipos_servicio() 
if __name__ == "__main__":
    main()
