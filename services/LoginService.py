from config.db_settings import BaseDeDatos
from repositories_crud.LoginRepository import LoginRepository
from tests import test_trabajador
from utils.horario import horario


class LoginService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.login_repository = LoginRepository(self.db)

    def registrar_trabajadores(self, email, numTrabajador):
        return self.login_repository.iniciar_trabajador(email, numTrabajador)

        # if datos == None:
        #     print("Sorry")
        # else:
        #     if datos[0] == email and datos[1] == numTrabajador:
        #         if datos[2] == "DEFLT":
        #             horario()
        #         elif datos[2] == "ADMIN":
        #             test_trabajador.main()
        #         return True
        #     else:
        #         return False
        
