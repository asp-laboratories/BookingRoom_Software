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
    
    # Actualizar datos de pago
    def actualizar_pago(self, montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo):
        if not self.db.conectar():
            return False
    
        try:
            cursor = self.db.cursor()

            cursor.execute("""
            UPDATE pago
            SET 
                montoPago = %s,
                descripcion = %s,
                fecha = %s,
                hora = %s,
                reservacion = %s,
                metodo_pago = %s,
                concepto_pago = %s,
                saldo = %s
                WHERE num = %s
                """, (montoPago, descripcion, fecha, hora, reservacion, metodo_pago, concepto_pago, saldo))

            self.db.connection.commit()
            print("El pago se actualizo correctamente")

        except Exception as error:
            print(f"Se encontro un error al actualizar el pago: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
    # Eliminar datos de pago
    def eliminar_pago(self, numPago):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM pago WHERE numPago = %s", (numPago,))
            self.db.connection.commit()

            print("Se elimino el pago correctamente")
            return True

        except Exception as error:
            print(f"Se encontro un error al eliminar pago: {error}")
            return False

        finally:
            cursor.close()
            self.db.desconectar()
    # Mostrar consulta solicitada
    def info_pago(self):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor(dictionary=True)
            #dentro de esta consulta el valor de la hora, no se como se pondria pero si ya es fija
            #colocar nada mas el valor y quitar el formato
            cursor.execute("""
                SELECT
                r.numReser AS CodigoReservacion,
                DATE_FORMAT(r.fechaEvento, "%d/%m/%Y") AS FechaEvento,
                dc.contNombre AS Nombre_Cliente,
                p.numPago AS NumeroPago,
                DATE_FORMAT(p.fecha, "%d/%m/%Y) AS FechaPago,
                DATE_FORMAT(p.hora, "%H:%i") AS HoraPago,
                mp.descripcion AS MetodoPago,
                p.concepto_pago AS ConceptoPago,
                p.montoPago AS MontoPago
                FROM pago AS p
                INNER JOIN reservacion AS r ON p.reservacion = r.numReser
                INNER JOIN datos_cliente AS dc ON r.datos_cliente = dc.RFC
                INNER JOIN metodo_pago AS mp ON p.metodo_pago = mp.codigoMe
                """)

            info = cursor.fetchall()
            return info

        except Exception as Error:
            print(f"No se pudieron obtener los pagos: {Error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    # Calcular los saldos de cada cliente, dependiendo el pago de la reservacion y el monto total
    def calcular_saldo(self, numReser):
        if not self.db.conectar():
            return False

        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute(
                "SELECT total FROM reservacion WHERE numReser = %s",
                (numReser,)
            )
            total = cursor.fetchone()["total"] #Esto del total, se pone para decir que se ocupa justo ese valor del diccionario en todo caso la consulta de arriba

            cursor.execute("""
                SELECT SUM(montoPago) AS pagos
                FROM pago 
                WHERE reservacion = %s
            """, (numReser,))
            pagos = cursor.fetchone()["pagos"] #al igual que aqui

            if pagos is None: # si no existe nungun valor en pagos osea lo de arriba, se convierte en 0 para que no se le reste nada
                pagos = 0
            
            saldo = total - pagos
            return saldo # returna este valor, que no se si se ocuparia otra cosa para que salga en la consulta

        except Exception as error:
            print(f"Existio un erro al calcular saldo: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()