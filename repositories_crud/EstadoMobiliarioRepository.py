
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
                            UPDATE esta_mob
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
<<<<<<< HEAD
=======

    def listar_mob_por_estado(self, esta_mob):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT 
                            mob.numMob,
                            mob.nombre,
                            imob.cantidad,
                            emob.descripcion
                            FROM inventario_mob as imob
                            INNER JOIN mobiliario as mob on imob.mobiliario = mob.numMob
                            INNER JOIN esta_mob as emob on imob.esta_mob = emob.codigoMob
                            WHERE emob.codigoMob = %s
                            """, (esta_mob,))
            
            resultado = cursor.fetchall()

            return resultado
        
        except Exception as error:
            print(f"Error al querer obtener el codigo de estado: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
>>>>>>> b750afa6492c60bbcec74608d5d37d6f8e1b43e7
