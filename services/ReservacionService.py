
from config.db_settings import BaseDeDatos
from repositories_crud.ReservacionRepository import ReservacionRepository
from models.Reservacion import Reservacion
from services.TipoMontajeService import TipoMontajeService
from services.TrabajadorServices import TrabajadorServices
from services.DatosClienteService import DatosClienteService
from services.EquipamentoService import EquipamentoService
from services.ServicioServices import ServicioService

class ReservacionService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.reservacion_repository = ReservacionRepository(self.db)
        self.tipo_montajeService = TipoMontajeService()
        self.TrabajadorService = TrabajadorServices()
        self.DatosClienteServices = DatosClienteService()
        self.EquipamientoService = EquipamentoService()
        self.ServicioService = ServicioService()

    # Metodos
    # Ingresar unicamente nombres de equipamientos y servicios
    def crear_reservacion(self, fechaReser, fechaEvento, horaInicio, horaFin, descripEvento, estimaAsistentes, tipo_montaje, trabajador, datos_cliente, datos_salon, equipamientos, servicios):
        # Comprobaciones del tipo de montaje, servicios, equipamientos, datos_salon, trabajador
        # Se tienen que agregar como pk
        numDatMon = self.tipo_montajeService.obtener_datos_montaje(tipo_montaje=tipo_montaje, datos_salon=datos_salon)
        rfcTraba = self.TrabajadorService.obtener_rfc_nombre(trabajador)
        rfcCliente = self.DatosClienteServices.obtener_rfc(datos_cliente)

        codigosEquipamientos = []
        if equipamientos != None:
            for equipamiento in equipamientos:
                equipamiento.equipamiento = self.EquipamientoService.obtener_codigo_equipamiento(equipamiento.equipamiento)
                print(equipamiento.equipamiento)
                codigosEquipamientos.append(equipamiento)

        codigosServicios = []
        if servicios != None:
            for servicio in servicios:
                servicio = self.ServicioService.obtener_codigo_servicio(servicio)
                codigosServicios.append(servicio)

        reservacion = Reservacion(fechaReser=fechaReser, fechaEvento=fechaEvento, horaInicio=horaInicio, horaFin=horaFin, descripEvento=descripEvento, estimaAsistentes=estimaAsistentes, datos_montaje=numDatMon, trabajador=rfcTraba, datos_cliente=rfcCliente, equipamientos=codigosEquipamientos, servicios=codigosServicios)

        return self.reservacion_repository.registrar_reservacion(reservacion)
    
    def info_reservacion(self, numReser):
        info = self.reservacion_repository.informacion_general_reservacion(numReser) # de aca obtenemos repetidos por los servicios, a mas servicios mas repetidos, unico caso de comprobacion ahi
        
        reservacion = {
                'numReser'           : info[0]['num_reser'],
                'fechaReser'         : info[0]['fecha_reser'],
                'cliNombreFiscal'    : info[0]['cliente'],
                'cliContacto'        : info[0]['cont_nombre'],
                'cliEmail'           : info[0]['cliente_email'],
                'fechaEvento'        : info[0]['fecha_even'],
                'horaInicioEvento'   : info[0]['hora_ini'],
                'horaFinEvento'      : info[0]['hora_fin'],
                'estadoReser'        : info[0]['esta_reser'],
                'nombreSalon'        : info[0]['nombre_salon'],
                'tipoMontaje'        : info[0]['montaje'],
                'estiamdoAsistentes' : info[0]['asistentes'],
                'servicios'          : []
            }
        
        if len(info) > 1:
            for registro in info:
                reservacion['servicios'].append(registro['servi'])

        return reservacion
        
    def reservaciones_fecha(self, fecha):
        return self.reservacion_repository.listar_reservacion_fecha(fecha)

    def obtener_total(self, numReser):
        total = self.reservacion_repository.obtener_total(numReser)
        return total['total']
    
    def reservacion_descripcion(self, numreser):
        decripcion = self.reservacion_repository.reservacion_descripcion(numreser)
        return decripcion['descripEvento']