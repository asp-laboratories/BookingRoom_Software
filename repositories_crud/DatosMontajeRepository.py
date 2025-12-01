
class DatosMontajeRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def obtener_codigo_datos_montaje(self, datos_montaje):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT numDatMon
                            FROM datos_montaje
                            WHERE tipo_montaje = %s and datos_salon = %s
                            """, (datos_montaje.tipo_montaje, datos_montaje.datos_salon))
            
            resultado = cursor.fetchone()

            return resultado
        
        except Exception as error:
            print(f"Erro al obtener datos de montaje: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()