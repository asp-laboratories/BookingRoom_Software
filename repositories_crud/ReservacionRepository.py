class ReservacionRepository:
    def __init__(self, db_configuration):
        self.db = db_configuration

    def _calcular_costo_mobiliario_y_actualizar_inventario(self, cursor, datos_montaje):
        cursor.execute(
            """
            SELECT mo.numMob, mo.costoRenta, mm.cantidad
            FROM montaje_mobiliario as mm
            INNER JOIN datos_montaje as dm on mm.datos_montaje = dm.numDatMon
            INNER JOIN mobiliario as mo on mm.mobiliario = mo.numMob
            WHERE mm.datos_montaje = %s
            """,
            (datos_montaje,),
        )
        costosMobiliarios = cursor.fetchall()

        totalMobiliarios = 0
        for mobiliario in costosMobiliarios:
            totalMobiliarios += mobiliario["costoRenta"] * mobiliario["cantidad"]
            numMob = mobiliario["numMob"]
            cantidad = mobiliario["cantidad"]

            cursor.execute(
                "UPDATE inventario_mob SET cantidad = cantidad - %s WHERE mobiliario = %s AND esta_mob = 'DISPO'",
                (cantidad, numMob),
            )
            cursor.execute(
                "INSERT INTO inventario_mob (mobiliario, esta_mob, cantidad) VALUES (%s, 'RESER', %s) ON DUPLICATE KEY UPDATE cantidad = cantidad + %s",
                (numMob, cantidad, cantidad),
            )
        return totalMobiliarios

    def _calcular_costo_equipamiento_y_actualizar_inventario(self, cursor, equipamientos):
        totalEquipamientos = 0
        if equipamientos:
            for equipamiento in equipamientos:
                cursor.execute(
                    "SELECT costoRenta FROM equipamiento WHERE numEquipa = %s",
                    (equipamiento.equipamiento,),
                )
                costoEquipa = cursor.fetchone()
                totalEquipamientos += costoEquipa["costoRenta"] * equipamiento.cantidad
                numEquipa = equipamiento.equipamiento
                cantidad = equipamiento.cantidad

                cursor.execute(
                    "UPDATE inventario_equipa SET cantidad = cantidad - %s WHERE equipamiento = %s AND esta_equipa = 'DISPO'",
                    (cantidad, numEquipa),
                )
                cursor.execute(
                    "INSERT INTO inventario_equipa (equipamiento, esta_equipa, cantidad) VALUES (%s, 'RESER', %s) ON DUPLICATE KEY UPDATE cantidad = cantidad + %s",
                    (numEquipa, cantidad, cantidad),
                )
        return totalEquipamientos

    def _calcular_costo_servicios(self, cursor, servicios):
        totalServicios = 0
        if servicios:
            for servicio in servicios:
                cursor.execute(
                    "SELECT costoRenta FROM servicio WHERE numServicio = %s",
                    (servicio,),
                )
                costoServicio = cursor.fetchone()
                totalServicios += costoServicio["costoRenta"]
        return totalServicios

    def _calcular_costo_salon(self, cursor, datos_montaje):
        cursor.execute(
            """
            SELECT ds.costoRenta
            FROM datos_salon as ds
            INNER JOIN datos_montaje as dm on dm.datos_salon = numSalon
            WHERE dm.numDatMon = %s
            """,
            (datos_montaje,),
        )
        costoSalon = cursor.fetchone()
        return costoSalon["costoRenta"] if costoSalon else 0

    def _insertar_reservacion(self, cursor, reservacion):
        cursor.execute(
            """
            INSERT INTO reservacion
            (fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes, subtotal, IVA, total, datos_montaje, trabajador, datos_cliente, esta_reser)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                reservacion.fechaReser,
                reservacion.fechaEvento,
                reservacion.horaInicio,
                reservacion.horaFin,
                reservacion.descripEvento,
                reservacion.estimaAsistentes,
                reservacion.subtotal,
                reservacion.IVA,
                reservacion.total,
                reservacion.datos_montaje,
                reservacion.trabajador,
                reservacion.datos_cliente,
                reservacion.esta_reser,
            ),
        )
        return cursor.lastrowid

    def _insertar_reser_equipos(self, cursor, numReser, equipamientos):
        if equipamientos:
            for equipa in equipamientos:
                cursor.execute(
                    "INSERT INTO reser_equipa (reservacion, equipamiento, cantidad) VALUES (%s, %s, %s)",
                    (numReser, equipa.equipamiento, equipa.cantidad),
                )

    def _insertar_reser_servicios(self, cursor, numReser, servicios):
        if servicios:
            for servicio in servicios:
                cursor.execute(
                    "INSERT INTO reser_servicio (reservacion, servicio) VALUES (%s, %s)",
                    (numReser, servicio),
                )

    def _actualizar_estado_salon(self, cursor, datos_montaje):
        cursor.execute(
            """
            SELECT ds.numSalon
            FROM datos_montaje as dm
            INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
            WHERE dm.numDatMon = %s
            """,
            (datos_montaje,),
        )
        resultado = cursor.fetchone()
        if resultado:
            numSalon = resultado["numSalon"]
            cursor.execute(
                "UPDATE datos_salon SET esta_salon = 'RESER' WHERE numSalon = %s",
                (numSalon,),
            )

    def registrar_reservacion(self, reservacion):
        cursor = None
        try:
            cursor = self.db.cursor()

            totalMobiliarios = self._calcular_costo_mobiliario_y_actualizar_inventario(cursor, reservacion.datos_montaje)
            totalEquipamientos = self._calcular_costo_equipamiento_y_actualizar_inventario(cursor, reservacion.equipamientos)
            totalServicios = self._calcular_costo_servicios(cursor, reservacion.servicios)
            totalSalon = self._calcular_costo_salon(cursor, reservacion.datos_montaje)

            reservacion.subtotal = totalEquipamientos + totalServicios + totalMobiliarios + totalSalon
            reservacion.IVA = reservacion.subtotal * 0.16
            reservacion.total = reservacion.IVA + reservacion.subtotal

            numReser = self._insertar_reservacion(cursor, reservacion)

            self._insertar_reser_equipos(cursor, numReser, reservacion.equipamientos)
            self._insertar_reser_servicios(cursor, numReser, reservacion.servicios)
            self._actualizar_estado_salon(cursor, reservacion.datos_montaje)

            self.db.connection.commit()
            return True

        except Exception as error:
            print(f"Error al registrar la reservacion: {error}")
            self.db.connection.rollback()
            return False

        finally:
            if cursor:
                cursor.close()

    def listar_reservacion_fecha(self, fecha):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT
                            DATE_FORMAT(re.fechaEvento, '%d / %m / %Y') as fecha,
                            TIME_FORMAT(re.horaInicio, '%H:%i') as horaInicio,
                            TIME_FORMAT(re.horaFin, '%H:%i') as horaFin,
                            ds.nombre as salon,
                            dc.nombreFiscal,
                            re.descripEvento,
                            re.estimaAsistentes
                            FROM reservacion as re
                            INNER JOIN datos_montaje as dm on re.datos_montaje = dm.numDatMon
                            INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
                            INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC
                            WHERE re.fechaEvento = %s
                            order by re.horaInicio
                            """,
                (fecha,),
            )

            resutlados = cursor.fetchall()

            return resutlados

        except Exception as error:
            print(f"Error al listar las reservaciones: {error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def buscar_reservaciones_cliente(self):
        pass

    def informacion_general_reservacion(self, numReser):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute(
                """SELECT * FROM reser_servicio where reservacion = %s""", (numReser,)
            )

            servicios = cursor.fetchall()

            if not servicios:
                cursor.execute(
                    """
                                SELECT
                                    re.numReser as num_reser,
                                    DATE_FORMAT(re.fechaReser, '%d / %m / %Y') as fecha_reser,
                                    dc.nombreFiscal as cliente,
                                    CONCAT(dc.contNombre, ' ', dc.contPriApellido, ' ', dc.contSegApellido)
                                    as cont_nombre,
                                    dc.email as cliente_email,
                                    DATE_FORMAT(re.fechaEVento, '%d / %m / %Y') as fecha_even,
                                    TIME_FORMAT(re.horaInicio, '%H:%i') as hora_ini,
                                    TIME_FORMAT(re.horaFin, '%H:%i') as hora_fin,
                                    er.codigoRes as esta_reser,
                                    ds.nombre as nombre_salon,
                                    tm.nombre as montaje,
                                    re.estimaAsistentes as asistentes
                                FROM reservacion as re
                                INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC 
                                INNER JOIN esta_reser as er on re.esta_reser = er.codigoRes
                                INNER JOIN datos_montaje as dm on dm.numDatMon = re.datos_montaje
                                INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon 
                                INNER JOIN tipo_montaje as tm on dm.tipo_montaje = tm.codigoMon 
                                WHERE re.numReser = %s
                                """,
                    (numReser,),
                )

            else:
                cursor.execute(
                    """
                                SELECT
                                    re.numReser as num_reser,
                                    DATE_FORMAT(re.fechaReser, '%d / %m / %Y') as fecha_reser,
                                    dc.nombreFiscal as cliente,
                                    CONCAT(dc.contNombre, ' ', dc.contPriApellido, ' ', dc.contSegApellido)
                                    as cont_nombre,
                                    dc.email as cliente_email,
                                    DATE_FORMAT(re.fechaEVento, '%d / %m / %Y') as fecha_even,
                                    TIME_FORMAT(re.horaInicio, '%H:%i') as hora_ini,
                                    TIME_FORMAT(re.horaFin, '%H:%i') as hora_fin,
                                    er.codigoRes as esta_reser,
                                    ds.nombre as nombre_salon,
                                    tm.nombre as montaje,
                                    re.estimaAsistentes as asistentes,
                                    ser.nombre as servi
                                FROM reservacion as re
                                INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC 
                                INNER JOIN esta_reser as er on re.esta_reser = er.codigoRes
                                INNER JOIN datos_montaje as dm on dm.numDatMon = re.datos_montaje
                                INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon 
                                INNER JOIN tipo_montaje as tm on dm.tipo_montaje = tm.codigoMon 
                                INNER JOIN reser_servicio as res on res.reservacion = re.numReser 
                                INNER JOIN servicio as ser on res.servicio = ser.numservicio
                                WHERE re.numReser = %s
                                """,
                    (numReser,),
                )

            resultados = cursor.fetchall()

            return resultados
        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
            return None
        finally:
            if cursor:
                cursor.close()

    def listar_reservaciones(self):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute("""
                            SELECT
                            descripEvento,
                            DATE_FORMAT(fechaEvento, '%d / %m / %Y') as fecha
                            FROM reservacion
                            order by fechaEvento
                            """)

            resutlados = cursor.fetchall()

            return resutlados

        except Exception as error:
            print(f"Error al listar las reservaciones: {error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def obtener_total(self, numReser):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT total
                            FROM reservacion
                            WHERE numReser = %s
                            """,
                (numReser,),
            )

            resultados = cursor.fetchone()

            return resultados

        except Exception as error:
            print(f"Error para obtener el total de reservacion: {error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def reservacion_descripcion(self, numReser):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
                            SELECT descripEvento
                            FROM reservacion
                            WHERE numReser = %s
                            """,
                (numReser,),
            )

            info = cursor.fetchone()

            return info

        except Exception as Error:
            print(f"No se pudo obtener la descripcion de la reseracion: {Error}")
            return None

        finally:
            if cursor:
                cursor.close()

    def obtener_fecha(self, fecha):
        cursor = None
        try:
            cursor = self.db.cursor()

            cursor.execute(
                """
SELECT
DATE_FORMAT(re.fechaEvento, '%d / %m / %Y') as fecha_evento,
TIME_FORMAT(re.horaInicio, '%H : %i') as hra_ini,
TIME_FORMAT(re.horaFin, '%H : %i') as hra_fin,
dc.nombreFiscal as cliente,
re.descripEvento as evento,
ds.nombre as salon,
re.estimaAsistentes as asistentes
FROM reservacion as re
INNER JOIN datos_montaje as dm on re.datos_montaje = dm.numDatMon
INNER JOIN datos_salon as ds on dm.datos_salon = ds.numSalon
INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC
WHERE fechaEvento = %s
""",
                (fecha,),
            )

            resultados = cursor.fetchall()

            return resultados

        except Exception as error:
            print(f"Error para obtener el total de reservacion: {error}")
            return None
        finally:
            if cursor:
                cursor.close()
    def listar_por_trabajador(self, rfc):
        cursor = None
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT
                    r.numReser,
                    DATE_FORMAT(r.fechaReser, '%d/%m/%Y') as fechaReser,
                    DATE_FORMAT(r.fechaEvento, '%d/%m/%Y') as fechaEvento,
                    r.descripEvento,
                    dc.nombreFiscal as cliente
                FROM reservacion as r
                JOIN datos_cliente as dc ON r.datos_cliente = dc.RFC
                WHERE r.trabajador = %s
                ORDER BY r.fechaEvento DESC
                """,
                (rfc,)
            )
            resultados = cursor.fetchall()
            return resultados
        except Exception as error:
            print(f"Error al listar reservaciones por trabajador: {error}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def listar_reservaciones_en_rango(self, start_date, end_date):
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT
                    r.numReser as id_reservacion,
                    r.fechaEvento as fecha_reser,
                    TIME_FORMAT(r.horaInicio, '%H:%i') as hora_inicio,
                    TIME_FORMAT(r.horaFin, '%H:%i') as hora_fin,
                    r.descripEvento as evento,
                    ds.nombre as nombre_salon,
                    ds.numSalon as id_salon
                FROM reservacion as r
                JOIN datos_montaje as dm ON r.datos_montaje = dm.numDatMon
                JOIN datos_salon as ds ON dm.datos_salon = ds.numSalon
                WHERE r.fechaEvento BETWEEN %s AND %s
                """,
                (start_date, end_date)
            )
            resultados = cursor.fetchall()
            return resultados
        except Exception as error:
            print(f"Error al listar reservaciones en rango: {error}")
            return None
        finally:
            if cursor:
                cursor.close()