import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories_crud.MobiliarioRepository import MobiliarioRepository
from models.Mobiliario import Mobiliario
from config.db_settings import BaseDeDatos

class mobiliarioService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.mobiliario_repository = MobiliarioRepository(self.db)

    # Metodos
    def registrar_mobiliario(self, numMob, nombre, costoRenta, stock, tipo_mob, trabajador):
        mobiliario = Mobiliario(numMob, nombre, costoRenta, stock, tipo_mob, trabajador)
        return self.mobiliario_repository.crear_mobiliario(mobiliario)
    
    def listar_mobiliarios(self): # Sin descripcion detallada de tipo, estado, trabajador
        print("Mobiliarios: ")
        mobiliarios = self.mobiliario_repository.listar_mobiliarios()

        print("Numero: \tNombre: \tCosto de Renta \tStock \t")
        for mobiliario in mobiliarios:
            print(f"{mobiliario['numMob']}\t{mobiliario['nombre']}\t{mobiliario['costoRenta']}\t{mobiliario['stock']}")
            
    def listar_mobiliario_detallado(self, mobiliario : int): 
        print(f"Mobiliario {mobiliario}")

        info_mob = self.mobiliario_repository.datos_especificos_mob(mobiliario)

        if not info_mob:
            print("No existen registros del mobiliario buscado")

        # Se imprimen datos repetibles (nombre, numero, stock)
        print(f"{info_mob[0]['numMob']}. {info_mob[0]['nombre']} \tHay un total de: {info_mob[0]['stock']} \tCosto de Renta: {info_mob[0]['costoRenta']}")

        # Se guardan en un lista aparte todas aquellas caracteristicas que no se repitan
        lista_carac = []
        for row in info_mob: # Se recorre todo el array buscando caracteristicas
            if row['nombreCarac'] not in lista_carac: # Se comprueban y guardan aquellas caracteristicas que no se repitan
                lista_carac.append(row['nombreCarac'])
        
        # Se imprimen todas las caracteristicas
        print("Caracteristicas:")
        contador = 1
        for i in lista_carac:
            print(f"{contador}. {i}")
            contador += 1

        # Analogamente, se hace lo mismo para los estados y cantidades de cada estado
        lista_estado = []
        for row in info_mob:
            if row['descripcion'] not in lista_estado:
                if not (row['cantidad'] == 0):
                    lista_estado.append(row['cantidad'])
                    lista_estado.append(row['descripcion'])
        contador = 0
        # Los estados y sus cantidades se guardan en un array plano, en este las posiciones pares son las cantidades y las posiciones impares son los estados
        for i in lista_estado:
            if (contador % 2) == 0: # Si es par la posicion se imprime la cantidad que hay en su respectivo estado
                print(f"Hay {i}", end=' ')
            else: # Si no lo es se imprime el estado correspondiente a la cantidad anterior
                print(f"en estado: {i}",end= "\n")
            contador +=1
    
if __name__ == "__main__":
    prueba = mobiliarioService()
    print(prueba.listar_mobiliario_detallado(1))