#from models.Mobiliario import Mobiliario
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db_settings import BaseDeDatos

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
                INSERT INTO mobiliario (nombre, costoRenta, stock, tipo_mob, trabajador)
                VALUES (%s, %s, %s, %s, 'rfc123') 
                """, (mobiliario.nombre, mobiliario.costoRenta, mobiliario.stock, mobiliario.tipo_mob,)) # Aca se tiene q modificar para poner el rfc de un trabajador
            
            numMob = cursor.lastrowid

            for carac in mobiliario.caracteristicas:
                cursor.execute("""INSERT INTO mob_carac (nombreCarac, tipo_carac) values (%s, %s)""", (carac.nombreCarac, carac.tipo_carac,))

                numCarac = cursor.lastrowid

                cursor.execute("""INSERT INTO caracteristicas (mob_carac, mobiliario) VALUES (%s, %s)""", (numCarac, numMob))
                
            cursor.execute("""INSERT INTO inventario_mob (mobiliario, esta_mob, cantidad) VALUES (%s, 'DISPO', %s)""", (numMob, mobiliario.stock,))
            self.db.connection.commit()

            print("Se añadio un nuevo mobiliario")
            return True
        except Exception as error:
            print(f"Error al crear un mobiliario: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
        
    def listar_mobiliarios(self): 
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                            SELECT 
                            mob.numMob,
                            mob.nombre,
                            esmob.descripcion,
                            imob.cantidad
                            FROM mobiliario as mob
                            INNER JOIN inventario_mob as imob on imob.mobiliario = mob.numMob
                            INNER JOIN esta_mob as esmob on imob.esta_mob = esmob.codigoMob
                           """)
            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al listar los mobiliarios: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
    
    def datos_especificos_mob(self, mobiliario):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute( """
                            SELECT 
                                mob.numMob as mobiliario,
                                mob.nombre as nombre,
                                mob.stock as cantidad,
                                mcarac.nombreCarac as caracteristica,
                                tcarac.nombreCarac as ti_caracteristica,
                                emob.descripcion as estado
                            FROM mobiliario as mob
                            INNER JOIN caracteristicas as carac on carac.mobiliario = mob.numMob
                            INNER JOIN mob_carac as mcarac on carac.mob_carac = mcarac.numCarac
                            INNER JOIN tipo_carac as tcarac on mcarac.tipo_carac = tcarac.codigoTiCarac
                            INNER JOIN inventario_mob as imobi on imobi.mobiliario = mob.numMob
                            INNER JOIN esta_mob as emob on imobi.esta_mob = emob.codigoMob
                            WHERE mob.numMob = %s
                            """, (mobiliario,))

            resultados = cursor.fetchall()
            return resultados

        except Exception as error:
            print(f"Error al listar los mobiliarios: {error}")
        
        finally:
            cursor.close()
            self.db.desconectar()
        
    def eliminar_mobiliario(self, numMob : int):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute(f"""
                            DELETE FROM inventario_mob
                            WHERE mobiliario = {numMob}""")
            cursor.execute(f"""
                            DELETE FROM caracteristicas
                            WHERE mobiliario = {numMob}""")
            cursor.execute(f"""
                            DELETE FROM mobiliario
                            WHERE numMob = {numMob}""")
            
            self.db.connection.commit()
        
        except Exception as error:
            print(f"Error al eliminar un mobiliario: {error}")

        finally:
            cursor.close()
            self.db.desconectar()
            return True
    
   # Actualizacion de datos (stock, nombre, costo de renta) requiere de la pk del mobiliario
    def actu_mob_datos(self, numMob, nombre, costoRenta, stock):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute(f"""
                            UPDATE mobiliario set
                            nombre = '{nombre}',
                            costoRenta = {costoRenta},
                            stock = {stock}
                            where numMob = {numMob}""")
            
            self.db.connection.commit()
            return True
        
        except Exception as error:
            print(f"Error al actualizar los datos del mobiliario: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_num_mob(self, nombre):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute(f"SELECT numMob FROM mobiliario WHERE descripcion like '%{nombre}%'")
            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener un estado de mobiliario: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def actu_mob_esta(self, numMob, cantidad, esta_mob1, esta_mob2): # Actualizacion del estado (y cantidad del mobiliario en ese estado)
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()
            cursor.execute(f"""SELECT * FROM inventario_mob WHERE mobiliario = {numMob} and esta_mob = '{esta_mob2}'""")
            resultados = cursor.fetchall()
            
            cursor.execute(f"""SELECT cantidad FROM inventario_mob WHERE mobiliario = {numMob} and esta_mob = '{esta_mob1}'""")
            canti = cursor.fetchone()

            stockA = canti['cantidad']

            if not resultados:
                cursor.execute(f"""INSERT INTO inventario_mob (mobiliario, esta_mob, cantidad) values ({numMob}, '{esta_mob2}', {cantidad})""")

                cursor.execute(f"""UPDATE inventario_mob set cantidad = {stockA - cantidad} WHERE mobiliario = {numMob} and esta_mob = '{esta_mob1}'""")

            else:
                cursor.execute(f"""UPDATE inventario_mob set cantidad = {resultados[0]['cantidad'] + cantidad} WHERE mobiliario = {numMob} and esta_mob = '{esta_mob2}'""")

                cursor.execute(f"""UPDATE inventario_mob set cantidad = {stockA - cantidad} WHERE mobiliario = {numMob} and esta_mob = '{esta_mob1}'""")
            
            self.db.connection.commit()
            return True
        
        except Exception as error:
            print(f"Error al actualizar el dato: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()

    # Actualizacion de carateristica especifica del mobiliario, se tiene que ingresar la caracteristica especifica con 
    # su pk, se pueden actualizar el nombre, su tipo o ambos
    def actu_mob_carac(self, numCarac, nombreCarac = None, tipo_carac = None): 
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            if not tipo_carac:
                cursor.execute(f"""
                                UPDATE mob_carac set nombreCarac = '{nombreCarac}' WHERE numCarac = {numCarac}
                                """)
                self.db.connection.commit()

            elif not nombreCarac:
                cursor.execute(f"""
                                UPDATE mob_carac set tipo_carac = '{tipo_carac}' WHERE numCarac = {numCarac}
                                """)
                self.db.connection.commit()

            else: 
                cursor.execute(f"""
                                UPDATE mob_carac set nombreCarac = '{nombreCarac}', tipo_carac = '{tipo_carac}' WHERE numCarac = {numCarac}
                                """)
                self.db.connection.commit()
            return True

        except Exception as error:
            print(f"Error al actualizar la caracteristica del mobiliario: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
 
    def caracteristicas_mobiliario(self, numMob):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute(f"""
                            SELECT
                            mbcarac.numCarac as numcarac,
                            tpcarac.nombreCarac as tpcarac,
                            mbcarac.nombreCarac as nombcarac
                            FROM caracteristicas as carac 
                            INNER JOIN mob_carac as mbcarac on carac.mob_carac = mbcarac.numCarac
                            INNER JOIN tipo_carac as tpcarac on mbcarac.tipo_carac = tpcarac.codigoTiCarac
                            WHERE carac.mobiliario = {numMob}
                            """)
            
            resultados = cursor.fetchall()

            return resultados
        
        except Exception as error:
            print(f"Error al mostrar las caracteristicas de un mobiliario: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def listar_tipos_carac(self):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            
            cursor.execute("SELECT * FROM tipo_carac")
            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al listar los tipos de caracteristicas: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_tipo_carac(self, nombreCarac):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor()

            cursor.execute(f"SELECT codigoTiCarac FROM tipo_carac WHERE nombreCarac like '%{nombreCarac}%'") 
            codigoTiCarac = cursor.fetchone()

            return codigoTiCarac

        except Exception as error:
            print(f"Error al obtener el codigo del tipo de caracteristica: {error}")
            return None 

        finally:
            cursor.close()
            self.db.desconectar()          

    #def obtener_esta_mob(self, descripcion): # Esta funcion se movio a EstadoMobiliarioRepository (ya modificado en el service)
    #    if not self.db.conectar():
    #        return None
    #    
    #    try:
    #        cursor = self.db.cursor()
    #
    #        cursor.execute(f"SELECT codigoMob FROM esta_mob WHERE descripcion like '{descripcion}%'")
    #        resultado = cursor.fetchone()
    #
    #        return resultado
    #
    #    except Exception as error:
    #        print(f"Error al obtener un estado de mobiliario: {error}")
    #        return None
    #    
    #    finally:
    #        cursor.close()
    #        self.db.desconectar()

    def obtener_tipo_por_carac(self, nombreCarac):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute(f"SELECT tc.nombreCarac FROM mob_carac as mc INNER JOIN tipo_carac as tc on mc.tipo_carac = tc.codigoTiCarac WHERE nombreCarac like '%{nombreCarac}%'")
            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener un estado de mobiliario: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def mobiliario_por_tipo(self, codigo_tipo_mob):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
    
            cursor.execute("""
                            SELECT
                            mob.numMob as numero,
                            tm.descripcion as descripcion,
                            mob.nombre as mobiliario,
                            mob.costoRenta as costoRenta
                            FROM mobiliario as mob
                            INNER JOIN tipo_mob as tm on mob.tipo_mob = tm.codigoTiMob
                            WHERE tm.codigoTiMob = %s
                            """, (codigo_tipo_mob,))
            
            resultados = cursor.fetchall()
    
            return resultados
        
        except Exception as error:
            print(f"Error al obtener mobiliario por tipo: {error}")
            return None
    
        finally:
            cursor.close()
            self.db.desconectar()

if __name__ == "__main__":
    conexcion = BaseDeDatos(database='BookingRoomLocal')
    prueba = MobiliarioRepository(conexcion)
    print(prueba.obtener_esta_mob(1, "dispo"))
