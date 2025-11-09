import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Trabajador import Trabajador

def main():
    print("--Registro de trabajadores--")
    rfc = input("Ingresa tu RFC: ")
    nombre = input("Ingresa tu nombre: ")
    apellido_paterno = input("Ingresa tu apellido paterno: ")
    apellido_materno = input("Ingresa tu apellido materno: ")
    matricula = int(input("Ingresa tu matricula: "))
    numero_emple = int(input("Ingresa tu numero de empleado: "))
    telefono = int(input("Ingresa tu numero de celular: "))
    email = input("Ingresa tu correo electronico: ")
    
    t1 = Trabajador(rfc,nombre,apellido_paterno,apellido_materno,matricula,numero_emple,telefono,email)
    print(t1)

if __name__ == "__main__":
    main()
