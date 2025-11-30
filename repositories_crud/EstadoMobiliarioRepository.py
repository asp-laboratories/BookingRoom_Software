
class EstadoMobiliarioRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration
    
    # Metodos
    def crear_estado_mobiliario(self, EstaMob):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            INSERT INTO esta_mob (codigoMob, descripcion)
                            values (%s, %s)
                            """, (EstaMob.codigoMob, EstaMob.descripcion))

            self.db.connection.commit()
            return True
        
        except Exception as error:
            print(f"Error al querer crear un nuevo estado de mobiliario: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
    
    def actu_esta_mob(self, esta_og_codigo, new_esta_descripcion):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            UPDATE estA_mob
                            SET descripcion = %s
                            WHERE codigoMob = %s
                            """, (new_esta_descripcion, esta_og_codigo))

            self.db.connection.commit()
            return True
        
        except Exception as error:
            print(f"Error al querer modificar la descripcion del estado: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_codigo_estado(self, descripcion):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT codigoMob
                            FROM esta_mob
                            WHERE descripcion LIKE %s
                            """, (f"{descripcion}%",))
            
            resultado = cursor.fetchone()
            print(resultado)
            return resultado
        
        except Exception as error:
            print(f"Error al querer obtener el codigo de estado: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()