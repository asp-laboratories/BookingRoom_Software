import mysql.connector as conector
from dotenv import load_dotenv
import os

load_dotenv()

class BaseDeDatos:
    # Constructor
    def __init__(self):
        try:
            self.database_config = {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": 3306,
                "user": os.getenv("DB_USER", "root"),
                "password": os.getenv("DB_PASSWORD", ""),
                "database": os.getenv("DB_NAME", ""),
            }
            self.connection = None
            print("Conexion establecida")
        except Exception as error:
            print(f"Conexion Fallida a la base de datos {error}")

    # Metodos
    def conectar(self):
        try:
            self.connection = conector.connect(**self.database_config)
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def desconectar(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def cursor(self, dictionary=True):
        try:
            if not self.connection or not self.connection.is_connected():
                print("Conexión perdida. Reconectando...")
                if not self.conectar():
                    print("Error: No se pudo restablecer la conexión.")
                    return None
            
            return self.connection.cursor(dictionary=dictionary)
        except Exception as e:
            print(f"Error al obtener el cursor: {e}")
            return None

    def show_tables(self):
        print("Mostrando tablas")
        try:
            cursor = self.cursor()
            cursor.execute("show tables")
            consulta = cursor.fetchall()
            for tabla in consulta:
                print(f"{tabla.values()}")
        except Exception as e:
            print(f"Error, imposible mostrar tablas: {e}")

    def show_databases(self):
        print("Mostrando Bases de Datos")
        try:
            cursor = self.cursor()
            cursor.execute("show databases")
            consulta = cursor.fetchall()
            for tabla in consulta:
                print(f"{tabla.values()}")
        except Exception as e:
            print(f"Error, imposible mostrar tablas: {e}")

    def show_columns(self, table):
        cursor = self.cursor()
        cursor.execute(f"desc {table}")
        consulta = cursor.fetchall()
        # print(consulta)
        for atributo in consulta:
            print(f"{atributo}")


if __name__ == "__main__":
    conexion = BaseDeDatos()
    conexion.conectar()
    conexion.show_tables()
    conexion.show_databases()
    conexion.show_columns("trabajador")
