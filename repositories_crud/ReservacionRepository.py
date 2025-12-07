
from repositories_crud.MobiliarioRepository import MobiliarioRepository
from repositories_crud.InventarioEquipaRepository import InventarioEquipaRepository


class ReservacionRepository:
    # Constructor
    def __init__(self, db_configuration):
        self.db = db_configuration
        self.mobRepository = MobiliarioRepository(self.db)
        self.InvenEquipamiento = InventarioEquipaRepository(self.db)

    # Metodos
    def registrar_reservacion(self, reservacion):
        if not self.db.conectar():
            return False
        
        try:
            cursor = self.db.cursor()
            
            # Para determinar el total a pagar es necesario tener el costo de renta de mobiliarios, equipamientos, servicios y el salon

            # Obtencion de costo del mobiliario
            cursor.execute( """
                            SELECT mob.numMob, mo.costoRenta, mm.cantidad
                            FROM montaje_mobiliario as mm
                            INNER JOIN datos_montaje as dm on mm.datos_montaje = dm.numDatMon
                            INNER JOIN mobiliario as mo on mm.mobiliario = mo.numMob
                            WHERE mm.datos_montaje = %s
                            """, (reservacion.datos_montaje,))
            costosMobiliarios = cursor.fetchall()

            totalMobiliarios = 0
            for mobiliario in costosMobiliarios:
                totalMobiliarios += (mobiliario['costoRenta'] * mobiliario['cantidad'])

                self.mobRepository.actu_mob_esta(mobiliario['numMob'], mobiliario['cantidad'], 'DISPO', 'RESER')
            
            # Obtencion de costos de equipamientos
            totalEquipamientos = 0
            if reservacion.equipamientos:
                for equipamiento in reservacion.equipamientos:
                    cursor.execute( """
                                    SELECT costoRenta
                                    FROM equipamiento
                                    WHERE numEquipa = %s
                                    """, (equipamiento.equipamiento,))
                    
                    costoEquipa = cursor.fetchone()

                    self.InvenEquipamiento.actualizar_estado_equipamiento(equipamiento.equipamiento, 'DISPO', 'RESER', equipamiento.cantidad)

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
                            SELECT ds.costoRenta
                            FROM datos_salon as ds
                            INNER JOIN datos_montaje as dm on dm.datos_salon = numSalon
                            WHERE dm.numDatMon = %s
                            """, (reservacion.datos_montaje,))
            costoSalon = cursor.fetchone()
            totalSalon = costoSalon['costoRenta']

            # Suma de los totales de cada apartado
            reservacion.subtotal = (totalEquipamientos + totalServicios + totalMobiliarios + totalSalon)
            reservacion.IVA = reservacion.subtotal * 0.16
            reservacion.total = reservacion.IVA + reservacion.subtotal

            # No se tiene por default el total, toca calcularlo aparte, pero antes de hacer el insert
            cursor.execute( """INSERT INTO reservacion
                            (fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes, subtotal, IVA, total, datos_montaje, trabajador, datos_cliente, esta_reser)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (reservacion.fechaReser, reservacion.fechaEvento, reservacion.horaInicio, reservacion.horaFin, reservacion.descripEvento, reservacion.estimaAsistentes, reservacion.subtotal, reservacion.IVA, reservacion.total, reservacion.datos_montaje, reservacion.trabajador, reservacion.datos_cliente, reservacion.esta_reser))
            
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
                                    INSERT INTO reser_servicio (reservacion, servicio)
                                    values (%s, %s)
                                    """, (numReser, servicio))

            self.db.connection.commit()

        except Exception as error:
            print(f"Error al registrar la reservacion: {error}")
            return False
        
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_reservacion_fecha(self, fecha):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
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
                            INNER JOIN datos_salon as ds dm.datos_salon = ds.numSalon
                            INNER JOIN datos_cliente as dc on re.datos_cliente = dc.RFC
                            WHERE re.fechaEvento = %s
                            order by re.horaInicio
                            """, (fecha,))
        
            resutlados = cursor.fetchall()

            return resutlados

        except Exception as error:
            print(f"Error al listar las reservaciones: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def buscar_reservaciones_cliente(self):
        pass

    def informacion_general_reservacion(self, numReser):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute("""SELECT * FROM reser_servicio where reservacion = %s""", (numReser,))

            servicios = cursor.fetchall()

            if not servicios:
                cursor.execute( """
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
                                """,(numReser,))

            else:
                cursor.execute( """
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
                                """,(numReser,))
                
            resultados = cursor.fetchall()

            return resultados
        except Exception as error:
            print(f"Error al listar los datos del salon: {error}")
        finally:
            cursor.close()
            self.db.desconectar()

    def listar_reservaciones(self):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
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
            cursor.close()
            self.db.desconectar()
            
    def obtener_total(self, numReser):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT total
                            FROM reservacion
                            WHERE numReser = %s
                            """, (f"{numReser}%",))
            
            resultados = cursor.fetchone()

            return resultados
        
        except Exception as error:
            print(f"Error para obtener el total de reservacion: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()

    def reservacion_descripcion(self, numReser):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()

            cursor.execute( """
                            SELECT descripEvento
                            FROM reservacion
                            WHERE numReser = %s
                            """, (numReser,))

            info = cursor.fetchone()

            return info

        except Exception as Error:
            print(f"No se pudo obtener la descripcion de la reseracion: {Error}")
            return None

        finally:
            cursor.close()
            self.db.desconectar()

    def obtener_fecha(self, fecha):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()

            cursor.execute( """
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
""", (fecha,))
            
            resultados = cursor.fetchall()

            return resultados
        
        except Exception as error:
            print(f"Error para obtener el total de reservacion: {error}")
            return None

if __name__ == "__main__":
    pass
