from models.Rol import Rol


class RolRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_rol(self, rol):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO rol (codigoRol, descripcion)
                VALUES (%s, %s)
            """,
                (rol.codigoRol, rol.descripcion),
            )

            self.db.connection.commit()
            print("Se añadio un rol")
            return True
        except Exception as error:
            print(f"Error al crear un rol: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_descripcion(self, descripcion):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT * FROM rol WHERE descripcion = %s
            """,
                (descripcion,),
            )
            resultado = cursor.fetchone()
            rol = Rol(
                codigoRol=resultado["codigoRol"], descripcion=resultado["descripcion"]
            )
            return rol
        except Exception as error:
            print(f"Error: {error}")
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

    def obtener_codigo_rol(self, rolDescripcion):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT codigoRol
                            FROM rol
                            WHERE descripcion = %s 
                            """,
                (rolDescripcion,),
            )

            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener el codigo del rol: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def trabajadores_rol(self, rol):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT 
                            concat(tra.nombre, ' ', tra.priApellido, ' ', tra.segApellido)
                            as nombre, /*Nombre*/
                            tra.numTrabajador as numTraba, /*Numero del trabajador*/
                            tra.RFC,
                            tra.email, /*Email*/
                            tele.telefono /*Telefono(s)*/
                            FROM trabajador as tra
                            INNER JOIN telefonos as tele on tele.trabajador = tra.RFC
                            INNER JOIN rol on tra.rol = rol.codigoRol
                            WHERE rol = %s
                            """,
                (rol,),
            )

            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al obtener los trabajadores de un rol: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
