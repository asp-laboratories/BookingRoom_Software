from models.Servicios import Servicio

class ServicioRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_servicio(self, servicio):
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

    def listar_servicio(self):
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

    def obtener_servicios_inner(self):
        """Obtiene libros con información básica del autor incluida"""
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    s.codigoSer as codigoSer,
                    s.nombre as servicio,
                    s.descripcion as descripcion,
                    s.costoRenta as costoRenta,
                    s.tipo_servicio as ts,
                    t.descripcion as tipo  
                FROM servicio as s
                INNER JOIN tipo_servicio as t  ON s.tipo_servicio = t.codigoTiSer
            """)
            
            results = cursor.fetchall()
            servicios = []
            
            for row in results:
                servicio = Servicio(
                    codigoSer=row['codigoSer'],
                    nombre=row['servicio'],
                    descripcion=row['descripcion'],
                    costo_renta=row['costoRenta'],
                    tipo_servicio=row['ts']
                )
                
                servicio.tipo_nombre = row['tipo']  # Información directa
                
                servicios.append(servicio)
            
            return servicios
            
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.db.desconectar()



        
        
