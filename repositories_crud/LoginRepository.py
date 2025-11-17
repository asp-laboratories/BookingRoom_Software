from models.Trabajador import Trabajador


class LoginRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def iniciar_trabajador(self, email, numTrabajador):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT * FROM trabajador WHERE email = %s AND numTrabajador = %s 
            """, (email, numTrabajador))
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
            
            info = []

            trabajador = Trabajador(
                rfc = resultado['RFC'],
                numTrabajador = resultado['numTrabajador'],
                nombre = resultado['nombre'],
                priApellido=resultado['priApellido'],
                segApellido=resultado['segApellido'],
                email=resultado['email'],
                codigoRol=resultado['rol']
            )

            info.append(trabajador.email)
            info.append(trabajador.numTrabajador)
            info.append(trabajador.codigoRol)

            return info
        except Exception as error:
            print(f"Error al encontrar los datos: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
