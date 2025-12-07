import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories_crud.MobiliarioRepository import MobiliarioRepository
from repositories_crud.TipoMobiliarioRepository import TipoMobiliarioRepository
from repositories_crud.EstadoMobiliarioRepository import EstadoMobiliarioRepository
from models.Mobiliario import Mobiliario
from models.MobCarac import MobCarac
from models.EstaMob import EstaMob
from models.TipoCarac import TipoCarac
from models.InventarioMob import InventarioMob
from config.db_settings import BaseDeDatos

class mobiliarioService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.mobiliario_repository = MobiliarioRepository(self.db)
        self.tipoMobiliario_repository = TipoMobiliarioRepository(self.db)
        self.estaMob_repository = EstadoMobiliarioRepository(self.db)

    # Metodos
    def registrar_mobiliario(self, nombre, costoRenta, stock, tipo_mob, caracteristicas):
        mobi = Mobiliario(nombre, costoRenta, stock, tipo_mob, caracteristicas)
        return self.mobiliario_repository.crear_mobiliario(mobi)
    
    def listar_mobiliarios(self): # Sin descripcion detallada de tipo, estado, trabajador
        print("Mobiliarios: ")
        mobiliarios = self.mobiliario_repository.listar_mobiliarios()

        return mobiliarios
            
    def info_detallada_mobiliario(self, mobiliario : int): 
        
        info_mob = self.mobiliario_repository.datos_especificos_mob(mobiliario)

        if info_mob:
            mob_info = {
                'numMob'    : info_mob[0]['numMob'],
                'nombre'    : info_mob[0]['nombre'],
                'costoRenta': info_mob[0]['costoRenta'],
                'stock'     : info_mob[0]['stock'],
                'caracs'    : [],
                'esta_mob'  : []
            }

            lista_apoyo_esta = []
            lista_apoyo_caracs = []

            # Pa obtener la caracteristica especifica algo asi como f"{mob_info['caracs'][#].tipo_carac}: {mob_info['caracs'][#].nombreCarac}" (checar test)
            # siendo el '#' el numero de la caracteristica en orden, en un array por lo que se lee primero el 0, luego el 1 y asi
            for row in info_mob:
                caracteristica = row['caracteristica']
                
                if caracteristica not in lista_apoyo_caracs:
                    tipo_carac = TipoCarac(row['tipo_carac'], caracteristica)
                    mob_carac = MobCarac(nombreCarac=caracteristica, tipo_carac=tipo_carac)
                    mob_info['caracs'].append(mob_carac)

                    lista_apoyo_caracs.append(caracteristica)
                
            
            # Analogamente, este aunque parezca un poco diferente tecnicamente hace lo mismo, 
                estado = row['descripcion']

                if estado not in lista_apoyo_esta:
                    esta_mb = EstaMob(codigoMob=row['codigoMob'], descripcion=row['descripcion'])
                    inventario = InventarioMob(esta_mob=esta_mb, cantidad=row['cantidad'])
                    mob_info['esta_mob'].append(inventario)

                    lista_apoyo_esta.append(estado)

            return mob_info
        else:
            print("No existen registros del mobiliario buscado")
            return None
 
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
        esta_og = self.estaMob_repository.obtener_codigo_estado(esta_mob_og)
        new_esta = self.estaMob_repository.obtener_codigo_estado(new_esta_mob)

        if not esta_og or not new_esta:
            print("Valores no validos de estados")
            return 
        
        self.mobiliario_repository.actu_mob_esta(numMob, cantidad, esta_og['codigoMob'], new_esta['codigoMob'])
        
    def caracteristicas_mob(self, numMob):
        print("Caracteristicas del mobiliario")
        
        caracteristicas = self.mobiliario_repository.caracteristicas_mobiliario(numMob)

        lista_caracteristicas = []

        for carac in caracteristicas:
            dic_carac = {
            'numCarac'  : carac['numcarac'],
            'nombCarac'  : carac['nombcarac'],
            'tipo_carac' : carac['tpcarac']
            }
            lista_caracteristicas.append(dic_carac)

        return lista_caracteristicas

    def obtener_tipo_carac(self, nombreCarac):
        resultado = self.mobiliario_repository.obtener_tipo_carac(nombreCarac)
        if not resultado:
            print("No se encontro este tipo de caracteristica") 
        else:
            return resultado['codigoTiCarac']

    def listar_tipo_carac(self):
        print("Listando tipos de caracteristicas")
        tipos = self.mobiliario_repository.listar_tipos_carac()

        for tipo in tipos:
            print(f"{tipo['nombreCarac']}",end="\t")
            
        print("\n")

    def obtener_mob_estado(self, esta_mob):
        print("Listando mobiliarios por su estado")
        esta_mob = self.estaMob_repository.obtener_codigo_estado(esta_mob)
        resultado =  self.estaMob_repository.listar_mob_por_estado(esta_mob['codigoMob'])
        return resultado

    def mob_por_tipo(self, numMob):
        return self.mobiliario_repository.mobiliario_por_tipo(numMob)

    def datos_mob(self, numMob):
        return self.mobiliario_repository.datos_especificos_mob(numMob)
    
    def stock_disponible(self, nombre, cantidad):
        numMob = self.mobiliario_repository.obtener_num_mob(nombre)
        disponiobles = self.mobiliario_repository.mobiliario_disponible(numMob['numMob'])
        if disponiobles == None:
            return False
        elif disponiobles['cantidad'] > cantidad:
            return True
        else:
            return False

if __name__ == "__main__":
    prueba = mobiliarioService()
    #prueba.listar_tipo_carac()
    #prueba.actu_carac_mob(1,"hhh", 'mater')
    prueba.actu_esta_mob(numMob=3,cantidad=10,esta_mob_og='Disponible',new_esta_mob='No Disponible')
    #print(prueba.obtener_tipo_carac('espec'))
    #print(prueba.caracteristicas_mob(1))
    #prueba.actu_esta_mob(numMob=1,cantidad=50,esta_mob_og='disponible',new_esta_mob='no disponible')
    #print(prueba.obtener_tipo_carac('espec'))
    #print(prueba.caracteristicas_mob(1))
    #print(prueba.obtener_mob_estado('Disponible'))
