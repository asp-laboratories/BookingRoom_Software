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
