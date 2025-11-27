
class ReservacionRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration

    # Metodos
    def registrar_reservacion(self, reservacion):
        if not self.db.conectar:
            return False
        
        try:
            cursor = self.db.cursor()
            
            # Para determinar el total a pagar es necesario tener el costo de renta de mobiliarios, equipamientos, servicios y el salon

            # Obtencion de costo del mobiliario
            cursor.execute( """
                            SELECT mo.costoRenta, mm.cantidad
                            FROM montaje_mobiliario as mm
                            INNER JOIN mobiliario as mo on mm.mobiliario = mo.numMob
                            WHERE mm.tipo_montaje = %s
                            """, (reservacion.tipo_montaje,))
            costosMobiliarios = cursor.fetchall()

            totalMobiliarios = 0
            for mobiliario in costosMobiliarios:
                totalMobiliarios += (mobiliario['costoRenta'] * mobiliario['cantidad'])
            
            # Obtencion de costos de equipamientos
            totalEquipamientos = 0
            if reservacion.equipamientos:
                for equipamiento in reservacion.equipamientos:
                    cursor.execute( """
                                    SELECT costoRenta
                                    FROM equipamiento
                                    WHERE eq.numEquipa = %s
                                    """, (equipamiento.equipamiento,))
                    costoEquipa = cursor.fetchone()
                    totalEquipamientos += (costoEquipa['costoRenta'] * equipamiento.cantidad)

            # Obtencion de costos de servicios
            totalServicios = 0
            if reservacion.servicios:
                for servicio in reservacion.servicios:
                    cursor.execute( """
                                    SELECT costoRenta
                                    FROM servicio
                                    WHERE numServicio = %s
                                    """, (servicio,))
                    costoServicio = cursor.fetchone()
                    totalServicios += costoServicio['costoRenta']

            # Obtencion de costo de renta del salon
            cursor.execute( """
                            SELECT costoRenta
                            FROM datos_salon
                            WHERE numSalon = %s
                            """, (reservacion.datos_salon,))
            costoSalon = cursor.fetchone()
            totalSalon = costoSalon['costoRenta']

            # Suma de los totales de cada apartado
            reservacion.subtotal = (totalEquipamientos + totalServicios + totalMobiliarios + totalSalon)
            reservacion.IVA = reservacion.subtotal * 0.16
            reservacion.total = reservacion.IVA + reservacion.subtotal

            # No se tiene por default el total, toca calcularlo aparte, pero antes de hacer el insert
            cursor.execute( """INSERT INTO reservacion
                            (fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaEvento, estimaAsistentes, subtotal, IVA, total, tipo_montaje, trabajador, datos_cliente, datos_salon)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (reservacion.fechaReser, reservacion.fechaEvento, reservacion.horaInicio, reservacion.descripEvento, reservacion.estimaAsistentes, reservacion.subtotal, reservacion.IVA, reservacion.total, reservacion.tipo_montaje, reservacion.trabajador, reservacion.datos_cliente, reservacion.datos_salon))
            
            numReser = cursor.lastrowid

            # Guardar equipamientos y servicios asignados a la reservacion

            # Guardando datos de equipamientos
            if reservacion.equipamientos:
                for equipa in reservacion.equipamientos:
                    cursor.execute( """
                                    INSERT INTO reser_equipa (reservacion, equipamiento, cantidad)
                                    values (%s, %s, %s)
                                    """, (numReser, equipa.equipamiento, equipa.cantidad))

            # Guardando datos de servicios
            if reservacion.servicios:
                for servicio in reservacion.servicios:
                    cursor.execute( """
                                    INSER INTO reser_servicio (reservacion, servicio)
                                    values (%s, %s)
                                    """, (numReser, servicio))

            self.db.connection.commit()

        except Exception as error:
            print(f"Error al registrar la reservacion: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()

    def eliminar_reservacion(self, numReser):
        pass

    def listar_reservaciones(self):
        pass

    def listar_reservacion_fecha(self):
        pass

    def buscar_reservaciones_cliente(self):
        pass

if __name__ == "__main__":
    pass