import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Servicios import Servicio, TipoServicio
   
def main():
    tipo_servicio_emp = TipoServicio("SEML","Servicio Empresarial")
    servicio_internet = Servicio("INT","Internet", 750.99, tipo_servicio_emp)
    print(f"Servicio: {servicio_internet.nombre}")
    print(f"Tipo de servicio: {servicio_internet.tipo_servicio.descripcion}")

if __name__ == "__main__":
    main()
