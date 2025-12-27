

class EquipamentoRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_equipamiento(self, equipamiento):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO equipamiento (nombre, descripcion, costoRenta, stock, esta_equipa, tipo_equipa)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    equipamiento.nombre,
                    equipamiento.descripcion,
                    equipamiento.costoRenta,
                    equipamiento.stock,
                    equipamiento.esta_equipa,
                    equipamiento.tipo_equipa,
                ),
            )

            self.db.connection.commit()
            print("Se añadio un equipamento")
        except Exception as error:
            print(f"Error al crear un equipamento: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
        return True

    def listar_equipamiento_informacion(self, numEquipa):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM equipamiento WHERE numEquipa = %s", (numEquipa,)
            )
            resultados = cursor.fetchone()

        except Exception as error:
            print(f"Error al listar los equipamentos: {error}")
            return None
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

    def listar_equipamiento(self):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM equipamiento")
            valores_equipamiento = cursor.fetchall()

        except Exception as error:
            print(f"Error al actualizar salon: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()

        return valores_equipamiento

    def actualizar_equipamientos(self, campo, numEquipa, valor):
        if not self.db.conectar():
            return False

        CAMPOS = {
            "Nombre": "nombre",
            "Costo de renta": "costoRenta",
            "Descripcion": "descripcion",
            "Cantidad": "stock",
            "Tipo de equipamiento": "tipo_equipa",
        }

        if campo not in CAMPOS:
            print("Error: Nombre de campo no válido o no permitido para actualización.")
            return False

        transformar_campo = CAMPOS[campo]

        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                f"""
                UPDATE equipamiento
                SET {transformar_campo} = %s 
                WHERE numEquipa =%s
           """,
                (
                    valor,
                    numEquipa,
                ),
            )
            self.db.connection.commit()
            print("Servicio actualizado correctamente")
            return True
        except Exception as error:
            print(f"Error al actualizar: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def eliminar_equipamiento(self, esta_equipa):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                DELETE FROM equipamiento
                WHERE esta_equipa = %s
                    """,
                (esta_equipa),
            )
            self.db.connection.commit()
            print(f"Se eliminaron datos del equipamiento: {esta_equipa}")

        except Exception as error:
            print(f"Ocurrio un error al eliminar: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
        return True

    def obtener_num_equipa(self, nombre):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                "SELECT numEquipa FROM equipamiento WHERE nombre = %s", (nombre,)
            )
            numEquipa = cursor.fetchone()

            return numEquipa

        except Exception as error:
            print(f"Error al mostrar el numero de equipamiento: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def listar_equipamientos_reser(self, numReser):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT 
                            equi.nombre,
                            req.cantidad
                            FROM reser_equipa as req
                            INNER JOIN equipamiento as equi on req.equipamiento = equi.numEquipa
                            WHERE reservacion = %s
                            """,
                (numReser,),
            )

            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al obtener el equipamiento de una reservacion: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def eliminar_registro_equipamiento(self, numEquipa):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
                DELETE FROM equipamiento
                WHERE numEquipa = %s
            """,
                (numEquipa,),
            )
            self.db.connection.commit()
            print("Equipamiento eliminado correctamente")
        except Exception as error:
            print(f"Error al eliminar equipamiento: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_disponibles(self, numEquipa):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT cantidad
                            FROM inventario_equipa
                            WHERE equipamiento = %s and esta_equipa = 'DISPO'
                            """,
                (numEquipa,),
            )

            resultado = cursor.fetchone()

            return resultado

        except Exception as error:
            print(f"Error al obtener la cantidad disponible del equipamiento: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
