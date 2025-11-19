from models.TipoEquipa import TipoEquipa
from models.Equipamiento import Equipamiento

class TipoEquipoRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def crear_tipo_equipamento(self, tipo_equipa):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor() 
            cursor.execute("""
                INSERT INTO tipo_equipa (codigoTiEquipa, descripcion)
                VALUES (%s, %s)
                """, (tipo_equipa.codigoTiEquipa, tipo_equipa.descripcion))
            
            self.db.connection.commit()
            print("Se añadio un tipo de equipamento")

        except Exception as error:

            print(f"Error al crear el tipo de equipamento: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
            return True

    
    def listar_tipo_equipamentos(self): 
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""SELECT * FROM tipo_equipa""")

            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los servicios: {error}")
            
        finally:
            cursor.close()
            self.db.desconectar()

        return resultados
    
    def obtener_equipamentoss_de_tipo(self, tipo_equipa):# Aca se mostrarian los equipamentos por tipo de equipamento
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute("""SELECT * FROM tipo_equipa WHERE codigoTiEquipa = %s""", (tipo_equipa,))
            data_tipo = cursor.fetchone()

            if not data_tipo:
                return None
             
            tipoE = TipoEquipa(
                codigoTiEquipa=data_tipo['codigoTiEquipa'],
                descripcion=['descripcion']
            )

            cursor.execute("""" SELECT * FROM equipamiento WHERE tipo_equipa = %s""", (tipo_equipa,))
            equipamientos_data = cursor.fetchall()

            for equipamiento_data in equipamientos_data:
                equipamiento = Equipamiento(
                    numEquipa= equipamiento_data['numEquipa'],
                    nombre= equipamiento_data['nombre'],
                    descripcion= equipamiento_data['descripcion'],
                    costoRenta= equipamiento_data['costoRenta'],
                    stock= equipamiento_data['stock'],
                    esta_equipa= equipamiento_data['esta_equipa'],
                    tipo_equipa= tipo_equipa
                )
                tipoE.equipamientos.append(equipamiento)
            
            return tipoE

        except Exception as error:
            print(f"Error al obtener los equipamentos: {error}")
            return None
        
        finally:
            self.db.desconectar()