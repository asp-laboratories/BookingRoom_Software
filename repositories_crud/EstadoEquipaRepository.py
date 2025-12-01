class EstadoEquipaRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration
    
    # Metodos
    def crear_estado_mobiliario(self, esta_equi):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            INSERT INTO esta_mob (codigoEquipa, descripcion)
                            values (%s, %s)
                            """, (esta_equi.codigoEquipa, esta_equi.descripcion))

            self.db.connection.commit()
            return True
        
        except Exception as error:
            print(f"Error al querer crear un nuevo estado de equipamiento: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()
    
    def actu_esta_equi(self, esta_og_codigo, new_esta_descripcion):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            UPDATE esta_equipa
                            SET descripcion = %s
                            WHERE codigoEquipa = %s
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
                            SELECT codigoEquipa
                            FROM esta_quipa
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
    



    def listar_equipa_por_estado(self, esta_e):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT 
                            eq.numEquipa as Numero,
                            eq.nombre as Nombre,
                            iequ.cantidad as Cantidad,
                            equi.descripcion as Estado
                            FROM inventario_equipa as iequ
                            INNER JOIN equipamiento as eq on iequ.equipamiento = eq.numEquipa
                            INNER JOIN esta_quipa as equi on iequ.esta_quipa = equi.codigoEquipa
                            WHERE equi.codigoEquipa = %s
                            """, (esta_e,))
            
            resultado = cursor.fetchall()

            return resultado
        
        except Exception as error:
            print(f"Error al querer obtener el codigo de equipamiento: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
        
    def actualizar_estado_equipa(self, codigoEquipa, descripcion):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                            UPDATE esta_equipa
                            SET descripcion = %s
                            WHERE codigoEquipa = %s
                            """, (descripcion, codigoEquipa))

            self.db.connection.commit()
            return True

        except Exception as error:
            print(f"Error al actualizar el estado del equipamiento: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
    
    def eliminar_estado_equipa(self, codigoEquipa):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            DELETE FROM esta_equipa
                            WHERE codigoEquipa = %s
                            """, (codigoEquipa,))

            self.db.connection.commit()
            return True

        except Exception as error:
            print(f"Error al eliminar el estado del equipamiento: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
