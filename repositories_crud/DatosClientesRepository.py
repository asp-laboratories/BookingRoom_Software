class DatosClientesRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_cliente(self, cliente):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO datos_cliente (RFC, contNombre, contPriApellido, contSegApellido, nombreFiscal, email, dirCalle, dirColonia, dirNumero, tipo_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)
            """, (cliente.RFC, cliente.contNombre, cliente.contPriApellido, cliente.contSegApellido ,cliente.nombreFiscal, cliente.email, cliente.dirColonia, cliente.dirCalle,cliente.dirNumero, cliente.tipo_cliente))
    
            self.db.connection.commit()
            print("Se añadio un cliente")
            return True
        except Exception as error:
            print(f"Error al crear un cliente: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_cliente(self):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM datos_cliente")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los clientes: {error}")
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados

    def actualizar(self, RFC, codigoRol):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE datos_cliente 
                SET rol = %s 
                WHERE RFC = %s
            """, (codigoRol, RFC))
            self.db.connection.commit()
            print("cliente actualizado exitosamente.")
            
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_rfc(self, nombreFiscal):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT rfc
                            FROM datos_cliente
                            WHERE nombreFiscal like %s
                            """, (f"{nombreFiscal}%",))
            
            resultados = cursor.fetachone

            return resultados
        
        except Exception as error:
            print(f"Error al obtener rfc del cliente: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
