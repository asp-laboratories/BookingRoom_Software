class PagoRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_pago(self, pago):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO pago (montoPago, descripcion, fecha, montoPago, no_pago, saldo, concepto_pago, metodo_pago, reservacion)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (pago.montoPago, pago.descripcion, pago.fecha, pago.montoPago, pago.no_pago, pago.saldo, pago.concepto_pago, pago.metodo_pago, pago.reservacion))
    
            self.db.connection.commit()
            print("Se añadio un salon")
            return True
        except Exception as error:
            print(f"Error al crear un salon: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_pagos(self):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pagos")
            resultados = cursor.fetchall()

        except Exception as error:
            print(f"Error al listar los pagos: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
        return resultados
