from models.Equipamiento import Equipamiento

class ServicioRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_equipamiento(self, equipamiento):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO servicio (codigoSer, nombre, descripcion, costoRenta, tipo_servicio)
                VALUES (%s, %s, %s, %s, %s)
            """, (servicio.codigoSer, servicio.nombre, servicio.descripcion, servicio.costo_renta, servicio.tipo_servicio))
    
            self.db.connection.commit()
            print("Se añadio un de servicio")
            return True
        except Exception as error:
            print(f"Error al crear un servicio: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_equipamiento(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM servicio")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los servicios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

