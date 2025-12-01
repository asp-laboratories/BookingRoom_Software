class TrabajadorRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_trabajador(self, trabajador):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO trabajador (RFC, numTrabajador, nombre, priApellido, segApellido, email, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (trabajador.rfc, trabajador.numTrabajador, trabajador.nombre ,trabajador.priApellido, trabajador.segApellido, trabajador.email, trabajador.codigoRol))
    
            self.db.connection.commit()
            print("Se añadio un trabajador")
            return True
        except Exception as error:
            print(f"Error al crear un trabajador: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_trabajador(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM trabajador")
            resultados = cursor.fetchall()
            return resultados
        except Exception as error:
            print(f"Error al listar los trabajadores: {error}")
        finally:
            cursor.close()
            self.db.desconectar()


    def sacar_trabajador(self, email):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT rfc FROM trabajador WHERE email = %s",(email,))
            resultados = cursor.fetchone()
            return resultados
        except Exception as error:
            print(f"Error al listar los trabajadores: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()



    def buscar_trabajadores(self, buscador):
        if not self.db.conectar():
            return None

        try:
            like = f"%{buscador}%"
            print(like)
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT t.RFC as RFC, CONCAT(t.nombre, ' ', t.priApellido, ' ', t.segApellido) as nombre, r.descripcion as rol  
                FROM trabajador as t
                INNER JOIN rol as r on t.rol = r.codigoRol
                WHERE nombre LIKE "%{buscador}%" 
            """)
            resultadoTraba = cursor.fetchall()

            return resultadoTraba
        except Exception as error:
            print(f"Error: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def actualizar_rol(self, RFC, codigoRol):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE trabajador 
                SET rol = %s 
                WHERE RFC = %s
            """, (codigoRol, RFC))
            self.db.connection.commit()
            print("Trabajador actualizado exitosamente.")
            
        except Exception as e:
            print(f"Error al actualizar trabajador: {e}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
