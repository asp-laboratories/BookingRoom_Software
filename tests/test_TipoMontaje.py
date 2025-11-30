import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.TipoMontajeService import TipoMontajeService

tipoMontaje = TipoMontajeService()

def crear_tipoMontaje():
    pass

if __name__ == "__main__":
    crear_tipoMontaje()