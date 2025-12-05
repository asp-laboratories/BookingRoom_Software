

class PagoRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion

    def crear_pago(self, pago):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO pago (montoPago, descripcion, fecha, hora, noPago, saldo, concepto_pago, metodo_pago, reservacion)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (pago.montoPago, pago.descripcion, pago.fecha, pago.hora, pago.noPago, pago.saldo, pago.concepto_pago, pago.metodo_pago, pago.reservacion))
    
            self.db.connection.commit()
            print("Se registro correctamente un pago")
            return True
        except Exception as error:
            print(f"Error al registrar el pago: {error}")
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
    
    def pagos_reservacion(self, numReser):
        if not self.db.conectar():
            return False
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT
                            re.numReser,
                            DATE_FORMAT(re.fechaEvento, '%d/%m/%Y')
                            as fechaEvento,
                            dc.nombreFiscal,
                            pa.noPago,
                            concat(DATE_FORMAT(pa.fecha, '%d/%m/%Y'), ' - ', TIME_FORMAT(pa.hora, '%H:%i'))
                            as tiempo_pago,
                            mp.descripcion as metodo_pago,
                            cp.descripcion as concetp_pago,
                            pa.montoPago,
                            pa.saldo
                            FROM pago as pa
                            INNER JOIN reservacion as re on pa.reservacion = re.numReser
                            INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC
                            INNER JOIN metodo_pago as mp on pa.metodo_pago = mp.codigoMe
                            INNER JOIN concepto_pago as cp on pa.concepto_pago = cp.codigoConc
                            WHERE re.numReser = %s
                            """, (numReser,))
            
            resultados = cursor.fetchall()
            
            return resultados

        except Exception as error:
            print(f"Error al listar los pagos: {error}")
            return False
        finally:
            cursor.close()
            self.db.desconectar()
    
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
    def info_pago(self, numReser):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor(dictionary=True)
            #dentro de esta consulta el valor de la hora, no se como se pondria pero si ya es fija
            #colocar nada mas el valor y quitar el formato
            cursor.execute( """
                            SELECT
                            r.numReser AS CodigoReservacion,
                            DATE_FORMAT(r.fechaEvento, "%d/%m/%Y") AS FechaEvento,
                            dc.contNombre AS Nombre_Cliente,
                            p.noPago AS NumeroPago,
                            DATE_FORMAT(p.fecha, "%d/%m/%Y") AS FechaPago,
                            DATE_FORMAT(p.hora, "%H:%i") AS HoraPago,
                            mp.descripcion AS MetodoPago,
                            p.concepto_pago AS ConceptoPago,
                            p.montoPago AS MontoPago
                            FROM pago AS p
                            INNER JOIN reservacion AS r ON p.reservacion = r.numReser
                            INNER JOIN datos_cliente AS dc ON r.datos_cliente = dc.RFC
                            INNER JOIN metodo_pago AS mp ON p.metodo_pago = mp.codigoMe
                            WHERE r.numReser = %s
                            """, (numReser,))

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
            return 
        

        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute(
                "SELECT total FROM reservacion WHERE numReser = %s",
                (numReser,)
            )
            total = cursor.fetchone()["total"] #Esto del total, se pone para decir que se ocupa justo ese valor del diccionario en todo caso la consulta de arriba
            print(total)
            cursor.execute("""
                SELECT SUM(montoPago) AS pagos
                FROM pago 
                WHERE reservacion = %s
            """, (numReser,))
            pagos = cursor.fetchone()["pagos"] #al igual que aqui
            print(pagos)
            if pagos is None: # si no existe nungun valor en pagos osea lo de arriba, se convierte en 0 para que no se le reste nada
                pagos = 0
            
            saldo = total - pagos
            print(saldo)
            return saldo # returna este valor, que no se si se ocuparia otra cosa para que salga en la consulta

        except Exception as error:
            print(f"Existio un erro al calcular saldo: {error}")
            return 
        
        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_no_pago(self, numReser):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT COUNT(noPago) as pagos
                            FROM pago
                            WHERE reservacion = %s
                            """, (numReser,))

            info = cursor.fetchone()

            return info

        except Exception as Error:
            print(f"No se pudieron obtener los pagos: {Error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()
