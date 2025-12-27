class MetodoPagoRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def obtener_codigo_metodo(self, desripcion):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT codigoMe
                            FROM metodo_pago
                            WHERE descripcion like %s
                            """,
                (f"{desripcion}%",),
            )

            resultados = cursor.fetchone()

            return resultados

        except Exception as error:
            print(f"Error obteniendo codigo de metodo de pago: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
