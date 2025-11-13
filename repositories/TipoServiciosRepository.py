class TipoServiciosRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_tipo_servicio(self, tipo_servicio):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO tipo_servicio (codigoTiSer, descripcion)
                VALUES (%s, %s)
            """, (tipo_servicio.codigoTiSer, tipo_servicio.descripcion))
    
            self.db.connection.commit()
            print("Se añadio un tipo de servicio")
            return True
        except Exception as error:
            print(f"Error al crear tipo de servicio: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_tipo_servicio(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_servicio")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los servicios: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados






