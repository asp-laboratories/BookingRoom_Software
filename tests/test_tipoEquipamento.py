import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.Obtener_Numeros import obt_int
from services.TipoEquipamientoService import TipoEquipamentoService

Tequipamento = TipoEquipamentoService()

def registrar_tipo():
    while True:
        respuesta = obt_int("\nAgregar un tipo de equipamento? \n1. Si \n2. No")
        match respuesta:
            case 1:
                codigo_equipa = input("Ingrese el codigo del tipo de equipamento: \n")
                descripcion_tEquipa = input("Ingrese la descripcion del tipo de equipamento: \n") 
                Tequipamento.registrar_tipo_equipamento(codigo_equipa, descripcion_tEquipa)
            case 2:
                print("Saliendo")
                break
            case _:
                print("Valor fuera de rango, intente de nuevo")

def mostrar_tipos():
    while True:
        respuesta = obt_int("\nMostrar los tipos de equipamentos: \n1. Si \n2. No")
        match respuesta:
            case 1:
                Tequipamento.listar_tipos_equipamentos()
            case 2:
                print("Saliendo")
                break
            case _:
                print("Valor fuera de rango, intente de nuevo")

def mostrar_equipamentos_tipo():
    while True:
        respuesta = obt_int("\nMostrar los equipamentos por tipo de equipamento: \n1. Si \n2. No")
        match respuesta:
            case 1:
                tipo_equipa = input("Ingrese el tipo de equipamento a buscar\n")
                Tequipamento.mostrar_equipamentos_tipo(tipo_equipa)
            case 2:
                print("Saliendo")
                break
            case _:
                print("Valor fuera de rango, intente de nuevo")

def main():
    print("Menu de Tipos de Equipamentos")
    while True:
        respuesta = obt_int("1. Registrar nuevo Tipo de Equipamento \n2. Listar Tipos de Equipamentos \n3. Listar Equipamentos por tipo de equipamento \n0. Salir")

        match respuesta:
            case 0:
                print("Saliendo")
                break
            
            case 1:
                registrar_tipo()
            
            case 2:
                mostrar_tipos()
            
            case 3:
                mostrar_equipamentos_tipo()

            case _:
                print("Valor fuera de rango, intente de nuevo")

if __name__ == "__main__":
    main()