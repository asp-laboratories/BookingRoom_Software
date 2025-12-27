class ReserEquiRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_reservacion_equipa(self, reser_equipa):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO reser_equipa (reservacion, equipamiento, cantidad)
                VALUES (%s, %s, %s)
            """,
                (
                    reser_equipa.reservacion,
                    reser_equipa.equipamiento,
                    reser_equipa.cantidad,
                ),
            )

            self.db.connection.commit()
            print("Se añadio al reser_equipa")
            return True
        except Exception as error:
            print(f"Error al crear un trabajador: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar__equipa(self, numReser):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """

SELECT
    re.descripEvento as desc_reser,
    DATE_FORMAT(re.fechaEvento, '%d / %m / %Y') as fecha_reser,
    dc.nombreFiscal as cliente,
    equi.nombre as equipa,
    req.cantidad as cantidad
FROM reservacion as re
INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC
INNER JOIN reser_equipa as req on req.reservacion = re.numReser
INNER JOIN equipamiento as equi on req.equipamiento = equi.numEquipa
WHERE re.numReser = %s
            """,
                (numReser,),
            )
            resultados = cursor.fetchall()
            return resultados
        except Exception as error:
            print(f"Error al listar los trabajadores: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
