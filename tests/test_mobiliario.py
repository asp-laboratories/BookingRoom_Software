import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.Obtener_Numeros import obt_int, obt_float
from models.Mobiliario import Mobiliario
from models.MobCarac import MobCarac
from services.mobiliarioService import mobiliarioService
from services.TipoMobiliarioService import TipoMobiliarioService

tipo_mobiliario = TipoMobiliarioService()
mobiliario = mobiliarioService()

def registrar_mobilario():
    nombre = input("Ingrese el nombre del mobiliario\n")
    costoRenta = obt_float("Ingrese el costo de renta por dia que tendra")
    stock = obt_int("Ingrese el stock total que tiene de este mobiliario")
    while True:
        print("Seleccione el tipo de mobiliario del que se trata")
        tipo_mobiliario.listar_tipos_mobiliarios()
        tipo_mob = input("")
        if not tipo_mobiliario.obtener_codigo(tipo_mob):
            print("Tipo de mobiliario no valido, intente de nuevo")
        else:
            tipo_mob = tipo_mobiliario.obtener_codigo(tipo_mob)
            
            print(tipo_mob)
            break
    
    caracteristicas = []
    
    canti_carac = obt_int("Ingrese el total de caracteristicas a ingresar")
    for i in range(1, canti_carac + 1):
        nombreCarac = input(f"Ingrese la caracteristica {i}\n")
        while True:
            print("Seleccione el tipo de caracteristica al que se refiere")
            mobiliario.listar_tipo_carac()
            tipo_carac = input()
            if not mobiliario.obtener_tipo_carac(tipo_carac):
                print("Tipo de caracteristica no valido")
            else:
                tipo_carac = mobiliario.obtener_tipo_carac(tipo_carac)
                print(tipo_carac)
                break

        caracteristica = MobCarac(nombreCarac, tipo_carac)
        caracteristicas.append(caracteristica)
    
    mobiliario.registrar_mobiliario(nombre, costoRenta, stock, tipo_mob, caracteristicas)
        
def mostrar_mobiliarios():
    mobi = mobiliario.listar_mobiliarios()
    if mobi:
        print("Numero: \tNombre: \tCosto de Renta \tStock \t")
        for mobili in mobi:
            print(f"{mobili['numMob']}\t{mobili['nombre']}\t{mobili['costoRenta']}\t{mobili['stock']}")

def info_detallada_mobiliario():
    print("Eliga un mobiliario a inspeccionar:")
    mostrar_mobiliarios()
    mobi = obt_int("")
    mobili = mobiliario.info_detallada_mobiliario(mobi)
    if mobili:
        print(f"{mobili['numMob']}. {mobili['nombre']} Costo de Renta: {mobili['costoRenta']} Stock Disponible: {mobili['stock']}")
        for caracteristica in mobili['caracs']:
            print(f"Tipo: {caracteristica.tipo_carac} Caracteristica: {caracteristica.nombreCarac}")
    
        for estado in mobili['esta_mob']:
            print(f"{estado.esta_mob}: {estado.cantidad}")
    else:
        print("No existen registros de ese mobiliario")

def actualizar_estado_mob():
    pass

def actualizar_caracteristica_mob():
    pass

def actualizar_mob():
    pass

def mostrar_mobiliario_tipo():
    pass

def main():
    registrar_mobilario()

if __name__ == "__main__":
    main()