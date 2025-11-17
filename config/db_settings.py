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

    def cursor(self, dictionary=True):
        if self.connection:
            return self.connection.cursor(dictionary=dictionary)
        return None
  




''' HACERLO CON DICCIONARIOS
    def show_tables(self):
        print("Mostrando tablas")
        try:
            cursor = self.cursor()
            cursor.execute('show tables')
            for i in cursor.fetchall():
                print(i)
        except:
            print("No te encuentras en una base de datos, imposible mostrar tablas")

    def show_databases(self):
        cursor = self.cursor()
        cursor.execute('show databases')
        for i in cursor.fetchall():
            print(i)

    def show_columns(self, table):
        resultado = self.execute(f'desc {table}')
        for i in resultado:
            print(i)

'''
