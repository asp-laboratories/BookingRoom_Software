from config.db_settings import BaseDeDatos
from repositories_crud.LoginRepository import LoginRepository


class LoginService:
    def __init__(self, db_instance):
        self.db = db_instance
        self.login_repository = LoginRepository(self.db)

    def autenticar_trabajador(self, email, numTrabajador):
        return self.login_repository.iniciar_trabajador(email, numTrabajador)
