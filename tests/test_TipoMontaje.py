import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.TipoMontajeService import TipoMontajeService

tipoMontaje = TipoMontajeService()

def crear_tipoMontaje():
    pass

def listar_tipos_montajes():
    tipos_montajes = tipoMontaje.listar_tipos_montajes()
    print("Codigo \t Nombre")
    for tipo in tipos_montajes:
        print(f"{tipo['codigoMon']} \t {tipo['nombre']}")

if __name__ == "__main__":
    listar_tipos_montajes()