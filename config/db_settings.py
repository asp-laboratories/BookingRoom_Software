import mysql.connector as conector

class BaseDeDatos():
    # Constructor
    def __init__(self, host = 'localhost', user = 'root', password = '', database = ''):
        try:
            self.database_config = {
                'host': host,
                'port': 3306,
                'user': user,
                'password': password,
                'database': database
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

    def cursor(self, dictionary= True):
        if self.connection:
            return self.connection.cursor(dictionary=dictionary)
        return None
  
    def show_tables(self):
        print("Mostrando tablas")
        try:
            cursor = self.cursor()
            cursor.execute('show tables')
            consulta = cursor.fetchall()
            for tabla in consulta:
                print(f"{tabla.values()}")
        except:
            print("Error, imposible mostrar tablas")

    def show_databases(self):
        print("Mostrando Bases de Datos")
        try:
            cursor = self.cursor()
            cursor.execute('show databases')
            consulta = cursor.fetchall()
            for tabla in consulta:
                print(f"{tabla.values()}")
        except:
            print("Error, imposible mostrar tablas")

    def show_columns(self, table):
        cursor = self.cursor()
        cursor.execute(f'desc {table}')
        consulta = cursor.fetchall()
        #print(consulta)
        for atributo in consulta:
            print(f"{atributo}")

if __name__ == "__main__":
    conexion = BaseDeDatos(database="bokkingroomlocal")
    conexion.conectar()
    conexion.show_tables()
    conexion.show_databases()
    conexion.show_columns('trabajador')


