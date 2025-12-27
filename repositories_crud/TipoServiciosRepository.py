from models.Servicios import Servicio
from models.TipoServicio import TipoServicio


class TipoServiciosRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_tipo_servicio(self, tipo_servicio):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO tipo_servicio (codigoTiSer, descripcion)
                VALUES (%s, %s)
            """,
                (tipo_servicio.codigoTiSer, tipo_servicio.descripcion),
            )

            self.db.connection.commit()
            print("Se añadio un tipo de servicio")
            return True
        except Exception as error:
            print(f"Error al crear tipo de servicio: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_tipo_servicio(self, descripcion):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                f"SELECT * FROM tipo_servicio WHERE descripcion LIKE '%{descripcion}%'"
            )
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los servicios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

    def descripcion_de_tipo(self, t_descripcion):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM tipo_servicio WHERE descripcion = %s", (t_descripcion,)
            )
            resultado = cursor.fetchone()

            if not resultado:
                return None

            simpleArreglo = []

            tipo = TipoServicio(
                codigoTiSer=resultado["codigoTiSer"],
                descripcion=resultado["descripcion"],
            )

            simpleArreglo.append(tipo.codigoTiSer)

            return tipo

        except Exception as error:
            print(f"Error al listar los servicios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_servicios_de_tipo(self, tipo_servicio):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM tipo_servicio WHERE codigoTiSer = %s", (tipo_servicio,)
            )
            tipo_data = cursor.fetchone()

            if not tipo_data:
                return None

            # Crear objeto Autor
            tipo = TipoServicio(
                codigoTiSer=tipo_data["codigoTiSer"],
                descripcion=tipo_data["descripcion"],
            )

            cursor.execute(
                "SELECT * FROM servicio WHERE tipo_servicio = %s", (tipo_servicio,)
            )
            servicios_data = cursor.fetchall()

            for servicio_data in servicios_data:
                servicio = Servicio(
                    nombre=servicio_data["nombre"],
                    descripcion=servicio_data["descripcion"],
                    costo_renta=servicio_data["costoRenta"],
                    tipo_servicio=servicio_data["tipo_servicio"],
                    tipo=tipo,
                )
                tipo.servicios.append(servicio)

            return tipo

        except Exception as e:
            print(f"Error al obtener los servicios: {e}")
            return None
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_codigo_tipo(self, nombre):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT codigoTiSer FROM tipo_servicio WHERE descripcion like %s",
                (f"{nombre}%",),
            )
            numServicio = cursor.fetchall()

            return numServicio
        except Exception as error:
            print(f"Error al mostrar el numero del servicio: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def listar_tipos_sevicios(self):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            SELECT *
                            FROM tipo_servicio
                            """)

            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error al listar los tipos de servicios: {error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
