
class TipoClienteRepository:
    # constructor
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    # MEtodos
    def listar_tipos_clientes(self):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT *
                            FROM tipo_cliente
                            """)
            
            resultado = cursor.fetchall()

            return resultado
        
        except Exception as error:
            print(f"Error al listar los tipos de cliente: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_clientes_por_tipo(self, tipo):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT 
                            dc.nombreFiscal,
                            dc.RFC,
                            tc.descripcion,
                            concat(dc.contNombre, ' ', dc.contPriApellido, ' ', dc.contSegApellido) as contacto,
                            dc.email,
                            concat(dc.dirCalle, ' ', dc.dirColonia, ' ', dc.dirNumero) as direccion,
                            tele.telefono
                            FROM datos_cliente as dc
                            INNER JOIN tipo_cliente as tc on dc.tipo_cliente = tc.codigoCli
                            INNER JOIN telefonos as tele on tele.datos_cliente = dc.RFC
                            WHERE tc.codigoCli = %s
                            """, ( tipo,))
            
            resultado = cursor.fetchall()

            return resultado
        
        except Exception as error:
            print(f"Error al listar los clientes bajo el tipo {tipo}: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_codigo_tipo_cliente(self, descripcion):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT codigoCli
                            FROM tipo_cliente
                            WHERE descripcion = %s
                            """, ( descripcion,))
            
            resultado = cursor.fetchone()

            return resultado
        
        except Exception as error:
            print(f"Error al obtener el codigo del tipo de cliente: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
