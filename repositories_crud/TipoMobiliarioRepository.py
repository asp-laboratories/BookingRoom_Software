import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.TipoMob import TipoMob
from models.Mobiliario import Mobiliario
from config.db_settings import BaseDeDatos

class TipoMobiliarioRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def crear_tipo_mobilario(self, tipo_mobiliario):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO tipo_mob (codigoTiMob, descripcion)
                VALUES (%s, %s)""", (tipo_mobiliario.codigoTiMob, tipo_mobiliario.descripcion))
    
            self.db.connection.commit()
            print("Se añadio un tipo de mobiliario")
        except Exception as error:
            print(f"Error al crear tipo de mobiliario: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
            return True

    def listar_tipos_mobiliarios(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_mob")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los tipos de mobiliarios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
            return resultados

    def obtener_mobiliarios_tipo(self, tipo_mob):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM tipo_mob WHERE codigoTiMob = %s", (tipo_mob,))
            tipo_data = cursor.fetchone()
            
            if not tipo_data:
                return None
            
            tipo = TipoMob(
                codigoTiMob=tipo_data['codigoTiMob'],
                descripcion=tipo_data['descripcion']
            )
            
            cursor.execute("SELECT * FROM mobiliario WHERE tipo_mob = %s", (tipo_mob,))
            mobiliarios_data = cursor.fetchall()
            
      
            for mobiliario in mobiliarios_data:
                mobiliario_data = Mobiliario(
                    numMob=mobiliario['numMob'],
                    nombre=mobiliario['nombre'],
                    costoRenta=mobiliario['costoRenta'],
                    stock=mobiliario['stock'],
                    tipo_mob=tipo
                )
                tipo.mobiliarios.append(mobiliario_data)  
            
            return tipo
            
        except Exception as e:
            print(f"Error al obtener los servicios: {e}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def codigo_tipo_mob(self, descripcion):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute(f"""
                            SELECT codigoTiMob
                            FROM tipo_mob
                            WHERE descripcion LIKE '{descripcion}%'
                            """)
            
            resultado = cursor.fetchone()        
            return resultado

        except Exception as error:
            print(f"Error al intentar obtener codigo del tipo de mobiliario: {error}")

        finally:
            cursor.close()
            self.db.desconectar()

if __name__ == "__main__":
    db = BaseDeDatos(database='BookingRoomLocal')
    pruebas = TipoMobiliarioRepository(db)
    print(pruebas.codigo_tipo_mob(''))
