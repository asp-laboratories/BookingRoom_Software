
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.Obtener_Numeros import obt_int

from services.EquipamentoService import EquipamentoService

equipamento = EquipamentoService()

def registro_equipamento():
    while True:
        numEquipa = obt_int("Ingrese el numero del equipamento")
        nombre = input("Ingrese el nombre del equipamento \n")
        descripcion = input("Introduzca la descripcion del equipamento \n")
        costoRenta = float(input("Ingrese el costo del equipamento \n")) # posible creacion de metodo para obtener numeros de punto flotante
        stock = obt_int("Ingrese el total de stock del equipamento")
        tipo_equipa = input("Ingrese el tipo de equipamento al que pertenece \n")
        if equipamento.registrar_equipamento(numEquipa= numEquipa, nombre= nombre, descripcion=descripcion, costoRenta= costoRenta, stock= stock, tipo_equipa= tipo_equipa):
            print("Equipamento creado correctamente")
            break
        else:
            print("No se pudo crear el equipamento intente de nuevo")

def main():
    print(f"{'':-<10}{' Menu de Equipamentos '}{'':-<10}")
    while True:
        respuesta = obt_int("1. Registrar un Equipamento nuevo \n2. Listar Equipamentos (sin descripcion) \n3. Listar Equipamentos (con descripcion) \n0. Salir")

        match respuesta:
            case 0:
                print("Saliendo")
                break
            case 1:
                print("Registro de un nuevo Equipamento") #  Por defualt se queda en disponivble
                registro_equipamento()
                
            case 2:
                print("Listando equipamentos")
                equipamento.listar_equipamentos()
            case 3:
                print("Listando equipamentos")
                equipamento.listar_equipamento_descripcion()
            case _:
                print("Valor fuera de rango, intentar de nuevo")


if __name__ == "__main__":
    main()