import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests import test_trabajador
from services.LoginService import LoginService
login = LoginService()

def main():
    email = input("Ingresa email: ")
    numTrabajador = input("Ingresa numero de trabajador: ")
    p = login.registrar_trabajadores(email, numTrabajador)
    if p:
        test_trabajador.main()
            

main()
