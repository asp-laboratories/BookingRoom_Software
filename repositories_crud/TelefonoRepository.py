class TelefonoRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_telefono(self, telefono):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO telefonos (telefono, datos_cliente, trabajador)
                VALUES ( %s, %s, %s)
            """,
                (telefono.telefono, telefono.datos_cliente, telefono.trabajador),
            )

            self.db.connection.commit()
            print("Se añadio un telefono")
            return True
        except Exception as error:
            print(f"Error al crear un telefono: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_telefono(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM telefonos")

            resultados = cursor.fetchall()
            return resultados

        except Exception as error:
            print(f"Error al listar los telefonos: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def listar_telefono_informacion(self, rfc):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
            SELECT t.telefono
            FROM telefonos AS t
            INNER JOIN datos_cliente AS dc ON t.datos_cliente = dc.RFC
            WHERE dc.RFC = %s
            """,
                (rfc,),
            )
            resultados = cursor.fetchall()
            return resultados

        except Exception as error:
            print(f"Error al listar los telefonos: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
