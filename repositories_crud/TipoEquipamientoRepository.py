from models.TipoEquipa import TipoEquipa
from models.Equipamiento import Equipamiento

class TipoEquipaRepository:
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
    
    def obtener_equipamentos_de_tipo(self, tipo_equipa):# Aca se mostrarian los equipamentos por tipo de equipamento
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
            cursor.close()
            self.db.desconectar()

    def descripcion_de_tipo(self,t_descripcion):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_equipa WHERE descripcion = %s",(t_descripcion,))
            resultado = cursor.fetchone()

            if not resultado:
                return None


            tipo = TipoEquipa(
                codigoTiEquipa=resultado['codigoTiEquipa'],
                descripcion=resultado['descripcion']
            )


            return tipo
            
        except Exception as error:
            print(f"Error al listar los servicios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def conjunto_equipamientos(self, descripcion):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute("""
select
te.descripcion as tipo_equipamiento,
e.nombre as equipamiento,
e.descripcion as descripcion,
e.costoRenta as costo
from equipamiento as e
inner join tipo_equipa as te on e.tipo_equipa = te.codigoTiEquipa
WHERE te.codigoTiEquipa = %s
            """, (descripcion,))
            resultado = cursor.fetchall()
            return resultado
        except Exception as error:
            print(f"Error al mostrar al mostrar conjunto: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
