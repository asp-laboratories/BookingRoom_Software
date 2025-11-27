import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories_crud.MobiliarioRepository import MobiliarioRepository
from models.Mobiliario import Mobiliario
from models.MobCarac import MobCarac
from config.db_settings import BaseDeDatos

class mobiliarioService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.mobiliario_repository = MobiliarioRepository(self.db)

    # Metodos
    def registrar_mobiliario(self, mobiliario):
        return self.mobiliario_repository.crear_mobiliario(mobiliario)
    
    def listar_mobiliarios(self): # Sin descripcion detallada de tipo, estado, trabajador
        print("Mobiliarios: ")
        mobiliarios = self.mobiliario_repository.listar_mobiliarios()

        print("Numero: \tNombre: \tCosto de Renta \tStock \t")
        for mobiliario in mobiliarios:
            print(f"{mobiliario['numMob']}\t{mobiliario['nombre']}\t{mobiliario['costoRenta']}\t{mobiliario['stock']}")
            
    def info_detallada_mobiliario(self, mobiliario : int): 
        print(f"Mobiliario {mobiliario}")

        info_mob = self.mobiliario_repository.datos_especificos_mob(mobiliario)

        if not info_mob:
            print("No existen registros del mobiliario buscado")
            return False
        
        mob = Mobiliario(numMob=info_mob[0]['numMob'], nombre=info_mob[0]['nombre'], costoRenta=info_mob[0]['costoRenta'], stock=info_mob[0]['stock'], tipo_mob=info_mob[0]['tipo_mob'])

        # Se imprimen datos repetibles (nombre, numero, stock)
        print(f"{info_mob[0]['numMob']}. {info_mob[0]['nombre']} \tHay un total de: {info_mob[0]['stock']} \tCosto de Renta: {info_mob[0]['costoRenta']}")

        for row in info_mob: # Se recorre todo el array buscando caracteristicas
            if row['nombreCarac'] not in mob.caracteristicas: # Se comprueban y guardan aquellas caracteristicas que no se repitan
                mob.caracteristicas.append(row['nombreCarac'])
        
        # Se imprimen todas las caracteristicas
        print("Caracteristicas:")
        contador = 1
        for i in mob.caracteristicas:
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
    
    def eliminar_mobiliario(self, numMob):
        print("Eliminando mobiliario")
        return self.mobiliario_repository.eliminar_mobiliario(numMob)

    def actu_datos_mob(self, numMob, new_nombre, new_costoRenta, new_stock):
        print("Actulizando datos de mobiliario")
        return self.mobiliario_repository.actu_mob_datos(numMob, new_nombre, new_costoRenta, new_stock)

    def actu_carac_mob(self, numCarac, nombreCarac, tipo_carac):
        print("Actualizando caracteristica del mobiliario")
        return self.mobiliario_repository.actu_mob_carac(numCarac, nombreCarac, tipo_carac)
    
    def actu_esta_mob(self, numMob, cantidad, esta_mob_og, new_esta_mob):
        print("Actualizando estado mobiliario")
        esta_og = self.mobiliario_repository.obtener_esta_mob(esta_mob_og)
        new_esta = self.mobiliario_repository.obtener_esta_mob(new_esta_mob)

        if not esta_og or not new_esta:
            print("Valores no validos de estados")
            return 
        
        self.mobiliario_repository.actu_mob_esta(numMob, cantidad, esta_og, new_esta)
        

    def caracteristicas_mob(self, numMob):
        print("Caracteristicas del mobiliario")
        
        caracteristicas = self.mobiliario_repository.caracteristicas_mobiliario(numMob)

        for carac in caracteristicas:
            print(f"{carac['numcarac']}. {carac['nombcarac']} de tipo {carac['tpcarac']}")

    def obtener_tipo_carac(self, nombreCarac):
        resultado = self.mobiliario_repository.obtener_tipo_carac(nombreCarac)
        if not resultado:
            print("No se encontro este tipo de caracteristica") 
        else:
            return resultado.strip()

    def listar_tipo_carac(self):
        print("Listando tipos de caracteristicas")
        tipos = self.mobiliario_repository.listar_tipos_carac()

        for tipo in tipos:
            print(f"{tipo['nombreCarac']}",end="\t")
            
        print("\n")

if __name__ == "__main__":
    conexcion = BaseDeDatos(database='BookingRoomLocal')
    prueba = mobiliarioService()
    #prueba.listar_tipo_carac()
    #print(prueba.obtener_tipo_carac('espec'))
    prueba.actu_esta_mob(15, 50, 'disponible', 'no disponible')