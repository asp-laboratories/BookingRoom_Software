
class RolRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_rol(self, rol):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO rol (codigoRol, descripcion)
                VALUES (%s, %s)
            """, (rol.codigoRol, rol.descripcion))
    
            self.db.connection.commit()
            print("Se añadio un rol")
            return True
        except Exception as error:
            print(f"Error al crear un rol: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_rol(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM rol")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los roles: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados
