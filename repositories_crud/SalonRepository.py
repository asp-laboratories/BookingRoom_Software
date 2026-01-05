class SalonRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_salon(self, salon):
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO datos_salon (nombre, costoRenta, ubiNombrePas, ubiNumeroPas, dimenLargo, dimenAncho, dimenAltura, mCuadrados, esta_salon)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    salon.nombre,
                    salon.costoRenta,
                    salon.ubiNombrePas,
                    salon.ubiNumeroPas,
                    salon.dimenLargo,
                    salon.dimenAncho,
                    salon.dimenAltura,
                    salon.mCuadrados,
                    salon.esta_salon,
                ),
            )

            self.db.connection.commit()
            print("Se añadio un salon")
            return True
        except Exception as error:
            print(f"Error al crear un salon: {error}")
            return False
        finally:
            if cursor:
                cursor.close()

    def listar_salones_2(self, numSalon):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM datos_salon WHERE numSalon = %s", (numSalon,))
            resultados = cursor.fetchone()

            return resultados
        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
            return None
        finally:
            if cursor:
                cursor.close()

    def listar_salones(self):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM datos_salon")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
            return None
        finally:
            if cursor:
                cursor.close()

        return resultados

    def listar_estados(self):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM esta_salon")
            resultados = cursor.fetchall()

            return resultados
        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
            return None
        finally:
            if cursor:
                cursor.close()

    def listar_salones_en_estado(self, estadoDesc):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
select
ds.numSalon as numero,
es.descripcion as estado,
ds.nombre as salon
from `datos_salon` as ds
inner join `esta_salon` as es on ds.esta_salon = es.codigoSal
where es.descripcion = %s
            """,
                (estadoDesc,),
            )
            resultados = cursor.fetchall()

            return resultados
        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
            return None
        finally:
            if cursor:
                cursor.close()

    def actualizar_salones(self, campo, numSalon, valor):
        CAMPOS = [
            "nombre",
            "costoRenta",
            "ubiNombrePas",
            "ubiNumeroPas",
            "dimenLargo",
            "dimenAncho",
            "dimenAltura",
            "mCuadrados",
        ]

        if campo not in CAMPOS:
            print(f"Error: El campo '{campo}' no es válido o no está permitido para actualización.")
            return False

        transformar_campo = campo

        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                f"""
                UPDATE datos_salon
                SET {transformar_campo} = %s 
                WHERE numSalon =%s
           """,
                (
                    valor,
                    numSalon,
                ),
            )
            self.db.connection.commit()
            print("Servicio actualizado correctamente")
            return True
        except Exception as error:
            print(f"Error al actualizar: {error}")
            return False
        finally:
            if cursor:
                cursor.close()

    def actualizar(self, numSalon, esta_salon):
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                UPDATE datos_salon 
                SET esta_salon = %s 
                WHERE numSalon = %s
            """,
                (esta_salon, numSalon),
            )
            self.db.connection.commit()
            print("Salon actualizado exitosamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar salon: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def obtener_num_salon(self, nombre):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """SELECT numSalon FROM datos_salon WHERE nombre = %s""", (nombre,)
            )
            numSalon = cursor.fetchone()

            return numSalon

        except Exception as error:
            print(f"Error al obtener el numero del salon: {error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def datos_montaje_salon(self, num_salon):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT
                            ds.nombre as salon,
                            CONCAT(ds.dimenLargo,'x',ds.dimenAncho,'x',ds.dimenAltura) as dimensiones,
                            ds.mCuadrados as metros_cuadrados,
                            tm.nombre as montaje,
                            tm.descripcion as descripcion_montaje,
                            dm.capacidad as capacidad
                            FROM datos_montaje as dm
                            INNER JOIN tipo_montaje as tm on dm.tipo_montaje = tm.codigoMon
                            INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
                            WHERE ds.numSalon = %s
                            """,
                (num_salon,),
            )

            resultados = cursor.fetchall()
            return resultados

        except Exception as error:
            print(f"Error al obtener datos de montaje del salón: {error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def eliminar_salon(self, numSalon):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
                DELETE FROM datos_salon
                WHERE numSalon = %s
            """,
                (numSalon,),
            )
            self.db.connection.commit()
            print("Salon eliminado correctamente")
            return True
        except Exception as error:
            print(f"Error al eliminar salon: {error}")
            return False
        finally:
            if cursor:
                cursor.close()

    def salon_disponible(self):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            SELECT ds.numSalon, DATE_FORMAT(re.fechaEvento, "%Y-%m-%d") as fecha
                            FROM reservacion as re
                            INNER JOIN datos_montaje as dm on re.datos_montaje = dm.numDatMon
                            INNER JOIN datos_salon as ds on dm.datos_salon= ds.numSalon
                            """)

            resultado = cursor.fetchall()

            return resultado

        except Exception as error:
            print(f"Error al listar los salones reservados: {error}")
            return None

        finally:
            if cursor:
                cursor.close()
