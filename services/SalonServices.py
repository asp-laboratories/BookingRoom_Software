from config.db_settings import BaseDeDatos
from models.DatosSalon import DatosSalon
from repositories_crud.SalonRepository import SalonRepository


class SalonServices:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.salon_repository = SalonRepository(self.db)
       
    def registrar_salones(self, numSalon, nombre, ubiNombrePas, ubiNumeroPas, dimenLargo, dimenAncho, dimenAltura, mCuadrados, esta_salon):
        salon = DatosSalon(numSalon, nombre, ubiNombrePas, ubiNumeroPas, dimenLargo, dimenAncho, dimenAltura, mCuadrados, esta_salon)
        return self.salon_repository.crear_salon(salon)

    def listar_salones(self):
        print("Salones: ")
        salon = self.salon_repository.listar_salones()
        print("Numero de salon:\t Nombre:\t Estado:")
        for row in salon:
            print(f"{row['numSalon']}\t\t\t {row['nombre']}\t\t\t {row['esta_salon']}")

    def listar_estados(self):
        print("Estados: ")
        estado = self.salon_repository.listar_estados()
        print("Codigo:\t Descripcion:\t")
        for row in estado:
            print(f"{row['codigoSal']}\t {row['descripcion']}")

    def actualizar_salon(self, numSalon, esta_salon):
         self.salon_repository.actualizar(numSalon, esta_salon)
