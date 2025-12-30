class InventarioEquipaRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def actualizar_estado_equipamiento(self, numEquipa, esta_og, new_esta, cantidad):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT *
                            FROM inventario_equipa
                            WHERE equipamiento = %s and esta_equipa = %s
                            """,
                (numEquipa, new_esta),
            )

            resultados = cursor.fetchall()

            if not resultados:
                cursor.execute(
                    """
                                INSERT INTO inventario_equipa (equipamiento, esta_equipa, cantidad) values
                                (%s, %s, %s)
                                """,
                    (numEquipa, new_esta, cantidad),
                )

                cursor.execute(
                    """SELECT cantidad FROM inventario_equipa WHERE equipamiento = %s and esta_equipa = %s""",
                    (numEquipa, esta_og),
                )

                oldCantidad = cursor.fetchone()
                newCantidad = oldCantidad["cantidad"] - cantidad

                cursor.execute(
                    """
                                UPDATE inventario_equipa set
                                cantidad = %s
                                WHERE equipamiento = %s and esta_equipa = %s
                                """,
                    (newCantidad, numEquipa, esta_og),
                )
            else:
                cursor.execute(
                    """SELECT cantidad FROM inventario_equipa WHERE equipamiento = %s and esta_equipa = %s""",
                    (numEquipa, new_esta),
                )
                oldCantidad = cursor.fetchone()
                newCantidad = oldCantidad["cantidad"] + cantidad

                cursor.execute(
                    """
                                UPDATE inventario_equipa set
                                cantidad = %s
                                WHERE equipamiento = %s and esta_equipa = %s
                                """,
                    (newCantidad, numEquipa, new_esta),
                )

                cursor.execute(
                    """SELECT cantidad FROM inventario_equipa WHERE equipamiento = %s and esta_equipa = %s""",
                    (numEquipa, esta_og),
                )

                oldCantidad = cursor.fetchone()
                newCantidad = oldCantidad["cantidad"] - cantidad

                cursor.execute(
                    """
                                UPDATE inventario_equipa set
                                cantidad = %s
                                WHERE equipamiento = %s and esta_equipa = %s
                                """,
                    (newCantidad, numEquipa, esta_og),
                )

            self.db.connection.commit()
            return True

        except Exception as error:
            print(f"Error al actualizar estado del equipamiento: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()

    def listar_estados_y_cantidades_por_equipo(self, num_equipo):
        if not self.db.conectar():
            return []
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT ie.esta_equipa, ie.cantidad, ee.descripcion
                FROM inventario_equipa ie
                JOIN estado_equipa ee ON ie.esta_equipa = ee.codigoEquipa
                WHERE ie.equipamiento = %s
                """,
                (num_equipo,)
            )
            resultados = cursor.fetchall()
            return resultados
        except Exception as error:
            print(f"Error al listar estados y cantidades por equipo: {error}")
            return []
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_cantidad_por_equipo_y_estado(self, num_equipo, estado_codigo):
        if not self.db.conectar():
            return 0
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT cantidad
                FROM inventario_equipa
                WHERE equipamiento = %s AND esta_equipa = %s
                """,
                (num_equipo, estado_codigo)
            )
            resultado = cursor.fetchone()
            if resultado:
                return resultado['cantidad']
            return 0
        except Exception as error:
            print(f"Error al obtener cantidad por equipo y estado: {error}")
            return 0
        finally:
            cursor.close()
            self.db.desconectar()
