class TrabajadorRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_trabajador(self, trabajador):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO trabajador (RFC, numTrabajador, nombre, priApellido, segApellido, email, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    trabajador.rfc,
                    trabajador.numTrabajador,
                    trabajador.nombre,
                    trabajador.priApellido,
                    trabajador.segApellido,
                    trabajador.email,
                    trabajador.codigoRol,
                ),
            )

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

    def sacar_trabajador(self, nombre):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT nombre FROM trabajador WHERE email = %s", (nombre,))
            resultados = cursor.fetchone()
            return resultados
        except Exception as error:
            print(f"Error al listar los trabajadores: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_rfc(self, nombre):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT rfc
                            FROM trabajador
                            WHERE nombre like %s
                            """,
                (f"{nombre}%",),
            )

            resutlado = cursor.fetchone()
            print(resutlado)
            return resutlado

        except Exception as error:
            print(f"Error al obtener el rfc del trabajador: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def buscar_trabajadores(self, buscador):
        if not self.db.conectar():
            return None

        try:
            like_pattern = f"%{buscador}%"
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    t.RFC, 
                    t.numTrabajador,
                    t.nombre, 
                    t.priApellido, 
                    t.segApellido, 
                    t.email,
                    r.descripcion as rol  
                FROM trabajador as t
                INNER JOIN rol as r on t.rol = r.codigoRol
                WHERE t.nombre LIKE %s
            """, (like_pattern,))
            resultadoTraba = cursor.fetchall()

            return resultadoTraba
        except Exception as error:
            print(f"Error: {error}")
            return None # Return None on error
        finally:
            cursor.close()
            self.db.desconectar()

    def buscar_trabajadores_por_reservacion(self, buscador):
        if not self.db.conectar():
            return None

        try:
            like_pattern = f"%{buscador}%"
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
select 
CONCAT(t.nombre, ' ',t.priApellido,' ', IFNULL(t.segApellido, ' ')) as trabajador,
dc.nombreFiscal as cliente,
r.numReser as reservacion,
DATE_FORMAT(r.fechaReser, '%d-%m-%Y ')as fecha,
r.descripEvento as descripcion
from reservacion as r
inner join trabajador as t on r.trabajador = t.RFC
inner join datos_cliente as dc on r.datos_cliente = dc.RFC
WHERE t.nombre LIKE %s 
""", (like_pattern,))
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
            cursor.execute(
                """
                UPDATE trabajador 
                SET rol = %s 
                WHERE RFC = %s
            """,
                (codigoRol, RFC),
            )
            self.db.connection.commit()
            print("Trabajador actualizado exitosamente.")

        except Exception as e:
            print(f"Error al actualizar trabajador: {e}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def actualizar_trabajador(self, campo, rfc, valor):
        if not self.db.conectar():
            return False

        CAMPOS_PERMITIDOS = ["nombre", "priApellido", "segApellido", "email"]
        if campo not in CAMPOS_PERMITIDOS:
            print(f"Error: El campo '{campo}' no es válido o no está permitido para actualización.")
            return False

        try:
            cursor = self.db.cursor()
            query = f"UPDATE trabajador SET {campo} = %s WHERE RFC = %s"
            cursor.execute(query, (valor, rfc))
            self.db.connection.commit()
            
            if cursor.rowcount == 0:
                print(f"Advertencia: No se encontró ningún trabajador con RFC '{rfc}' para actualizar.")
                return False

            print(f"Trabajador con RFC {rfc} actualizado correctamente en el campo {campo}.")
            return True
        except Exception as error:
            print(f"Error al actualizar trabajador: Failed to edit, Expected 1 occurrence but found 7 for old_string in file: /home/luisdgr/Descargas/BookingRoom_Software/repositories_crud/TrabajadorRepository.py")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_rfc_por_identificador(self, termino_busqueda):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            # Intenta buscar por RFC o por numTrabajador
            cursor.execute(
                """
                SELECT RFC FROM trabajador
                WHERE RFC = %s OR numTrabajador = %s
                """,
                (termino_busqueda, termino_busqueda)
            )
            resultado = cursor.fetchone()
            if resultado:
                return resultado['RFC']
            return None
        except Exception as error:
            print(f"Error al obtener RFC por identificador: Failed to edit, Expected 1 occurrence but found 8 for old_string in file: /home/luisdgr/Descargas/BookingRoom_Software/repositories_crud/TrabajadorRepository.py")
            return None
        finally:
            cursor.close()
            self.db.desconectar()
