
class ConceptoPagoRepository:
    # Constructor 
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def obtener_codigo_concepto(self, desripcion):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT codigoConc
                            FROM concepto_pago
                            WHERE descripcion like %s
                            """, (f"{desripcion}%",))
            
            resultados = cursor.fetchone()
            print(resultados)
            return resultados
        
        except Exception as error:
            print(f"Error obteniendo codigo del concepto de pago: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()