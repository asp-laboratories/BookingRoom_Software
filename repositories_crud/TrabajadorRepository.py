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

        except Exception as error:
            print(f"Error al listar los trabajadores: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

    def actualizar(self, RFC, codigoRol):
        if not self.db.conectar():
            return None
        
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
