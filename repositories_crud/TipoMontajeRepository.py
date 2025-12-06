
class TipoMontajeRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration
    
    # Metodos
    def listar_tipos_montajes(self):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute( """
                            SELECT * FROM tipo_montaje
                            """)
            
            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al listar los tipos de montaje: {error}")
            return None
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_salones_tipo_montaje(self, codigoMon):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute( """
                            SELECT *
                            FROM tipo_montaje as tm
                            INNER JOIN datos_montaje as dm on dm.tipo_montaje = tm.codigoMon
                            INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
                            WHERE codigoMon = %s
                            """, (codigoMon,))

            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener el codigo del montaje: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()   
    
    def obtener_codigo_montaje(self, nombreTipo):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute( """
                            SELECT codigoMon
                            FROM tipo_montaje
                            WHERE nombre = %s
                            """, (nombreTipo,))

            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener el codigo del montaje: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def mobiliarios_por_montaje(self, codigoMon):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute( """
                            SELECT
                                tm.nombre as tipo_montaje,
                                ds.nombre as salon,
                                mob.nombre as mobiliario,
                                mm.cantidad as cantidad
                            FROM datos_montaje as dm
                            INNER JOIN montaje_mobiliario as mm on mm.datos_montaje = dm.numDatMon
                            INNER JOIN tipo_montaje as tm on dm.tipo_montaje = tm.codigoMon
                            INNER JOIN mobiliario as mob on mm.mobiliario = mob.numMob
                            INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
                            WHERE tm.codigoMon = %s
                            """, (codigoMon,))

            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al listar los tipos de montaje: {error}")
            return None
        finally:
            cursor.close()
            self.db.desconectar()

    def ingresar_datos_montaje(self, datos_montaje):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO datos_montaje (capacidad, tipo_montaje, datos_salon)
                VALUES ( %s, %s, %s)
            """, (datos_montaje.capacidad, datos_montaje.tipo_montaje, datos_montaje.datos_salon))
    
            self.db.connection.commit()
            print("Se añadio informacion a datos_montaje")
            return True
        except Exception as error:
            print(f"Error al añadir informacion: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
