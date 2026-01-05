from models.Trabajador import Trabajador


class LoginRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def iniciar_trabajador(self, email, numTrabajador):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT * FROM trabajador WHERE email = %s AND numTrabajador = %s 
            """,
                (email, numTrabajador),
            )
            resultado = cursor.fetchone()

            if not resultado:
                return None

            trabajador = Trabajador(
                rfc=resultado["RFC"],
                numTrabajador=resultado["numTrabajador"],
                nombre=resultado["nombre"],
                priApellido=resultado["priApellido"],
                segApellido=resultado["segApellido"],
                email=resultado["email"],
                codigoRol=resultado["rol"],
            )
            return trabajador

        except Exception as error:
            print(f"Error al encontrar los datos: {error}")
            return None

        finally:
            if cursor:
                cursor.close()
