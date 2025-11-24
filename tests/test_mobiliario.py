import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.Obtener_Numeros import obt_int
from services.mobiliarioService import mobiliarioService

def registrar_mobilario():
    nombre = input("Ingrese el nombre del mobiliario\n")
    costoRenta = input("Ingrese el costo de renta por dia que tendra\n")
    stock = input("Ingrese el stock total que tiene de este mobiliario\n")
    print("Seleccione el tipo de mobiliario del que se trata")
    

def main():
    
    pass

if __name__ == "__main__":
    main()