#from models.Mobiliario import Mobiliario

class MobiliarioRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration
    
    # Metodos
    def crear_mobiliario(self, mobiliario):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO mobiliario (numMob, nombrem costoRenta, stock, tipo_mob, trabajador)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (mobiliario.numEquipa, mobiliario.nombre, mobiliario.costoRenta, mobiliario.stock, mobiliario.tipo_mob, mobiliario.trabajador))

            self.db.connection.commit()
            print("Se añadio un nuevo mobiliario")
        except Exception as error:
            print(f"Error al crear un mobiliario: {error}")
        
        finally:
            cursor.close()
            self.db.desconectar()
        
        return True
    
    def listar_mobiliarios(self): 
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM mobiliario")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los mobiliarios: {error}")
        
        finally:
            cursor.close()
            self.db.desconectar()

        return resultados
    
    def datos_especificos_mob(self, mobiliario):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(f"""SELECT 
                        mob.numMob,
                        mob.nombre,
                        mob.stock,
                        mob.costoRenta,
                        tcarac.nombreCarac,
                        mcarac.nombreCarac,
                        imobi.cantidad,
                        emob.descripcion
                        FROM mobiliario as mob
                        INNER JOIN caracteristicas as carac on carac.mobiliario = mob.numMob
                        INNER JOIN mob_carac as mcarac on carac.mob_carac = mcarac.numCarac
                        INNER JOIN tipo_carac as tcarac on mcarac.tipo_carac = tcarac.codigoTiCarac
                        INNER JOIN inventario_mob as imobi on imobi.mobiliario = mob.numMob
                        INNER JOIN esta_mob as emob on imobi.esta_mob = emob.codigoMob
                        WHERE mob.numMob = {mobiliario}""")

            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los mobiliarios: {error}")
        
        finally:
            cursor.close()
            self.db.desconectar()
            return resultados

    