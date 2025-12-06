import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.TipoMontajeService import TipoMontajeService

tipo_montaje = TipoMontajeService()

def crear_tipoMontaje():
    pass

def listar_tipos_montajes():
    tipos_montajes = tipo_montaje.listar_tipos_montajes()
    print("Codigo \t Nombre")
    for tipo in tipos_montajes:
        print(f"{tipo['codigoMon']} \t {tipo['nombre']}")

def mostrar_mobiliarios_montaje(montaje):
    tipoMontaje = tipo_montaje.listar_mobiliarios_montaje(montaje)
    for montaje in tipoMontaje:
        print(montaje['nombre'])
        for mobi in montaje['mobiliarios']:
            print(f"{mobi.mobiliario}: cantidad {mobi.cantidad}", end='\t')
        print()

def obtener_numdatmon(tipo_motanej, salon):
    print(tipo_montaje.obtener_datos_montaje(tipo_motanej, salon))

if __name__ == "__main__":
    mostrar_mobiliarios_montaje('Banquete')