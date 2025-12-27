from config.db_settings import BaseDeDatos
from models.DatosSalon import DatosSalon
from repositories_crud.SalonRepository import SalonRepository


class SalonServices:
    def __init__(self):
        self.db = BaseDeDatos(database="BookingRoomLocal")
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.salon_repository = SalonRepository(self.db)

    def registrar_salones(
        self,
        nombre,
        costoRenta,
        ubiNombrePas,
        ubiNumeroPas,
        dimenLargo,
        dimenAncho,
        dimenAltura,
        m2,
    ):
        salon = DatosSalon(
            nombre,
            costoRenta,
            ubiNombrePas,
            ubiNumeroPas,
            dimenLargo,
            dimenAncho,
            dimenAltura,
            m2,
        )
        return self.salon_repository.crear_salon(salon)

    def listar_salones_informacion(self, numSalon):
        print("Salones: ")
        salon = self.salon_repository.listar_salones_2(numSalon)
        return salon

    def listar_salones(self):
        return self.salon_repository.listar_salones()

        # print("Numero de salon:\t Nombre:\t Estado:")
        # for row in salon:
        #     print(f"{row['numSalon']}\t\t\t {row['nombre']}\t\t\t {row['esta_salon']}")

    def listar_estados(self):
        print("Estados: ")
        return self.salon_repository.listar_estados()
        # print("Codigo:\t Descripcion:\t")
        # for row in estado:
        #     print(f"{row['codigoSal']}\t {row['descripcion']}")

    def actualizar_campos(self, campo, numSalon, valor):
        return self.salon_repository.actualizar_salones(campo, numSalon, valor)

    def actualizar_salon(self, numSalon, esta_salon):
        self.salon_repository.actualizar(numSalon, esta_salon)

    def obtener_codigo_salon(self, nombreSalon):
        salon = self.salon_repository.obtener_num_salon(nombreSalon)
        return salon["numSalon"]

    def datos_montaje(self, numero_salon):
        return self.salon_repository.datos_montaje_salon(numero_salon)

    def eliminar_salones(self, numSalon):
        self.salon_repository.eliminar_salon(numSalon)

    def salon_disponible(self):
        return self.salon_repository.salon_disponible()

    def salon_en_estado(self, estadoD):
        return self.salon_repository.listar_salones_en_estado(estadoD)
