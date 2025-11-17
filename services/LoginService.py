from config.db_settings import BaseDeDatos
from repositories_crud.LoginRepository import LoginRepository


class LoginService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.login_repository = LoginRepository(self.db)

    def registrar_trabajadores(self, email, numTrabajador):
        datos = self.login_repository.iniciar_trabajador(email, numTrabajador)

        if datos == None:
            print("Sorry")
        else:
            if datos[0] == email and datos[1] == numTrabajador:
                if datos[2] == "DEFLT":
                    print("usuario default")
                return True
            else:
                return False
        
