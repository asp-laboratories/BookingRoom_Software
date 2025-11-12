import mysql.connector as conector

class conexion():
    # Constructor
    def __init__(self, host = 'localhost', user = 'root', password = '', database = ''):
        try:
            self.__mybd = conector.connect(
                host= host,
                user= user,
                password= password,
                port= 3306,
                database= database
            )

            self.__connection = None
            self.__cursor = self.__mybd.cursor()
            print("Conexion establecida")
        except:
            print("Conexion Fallida a la base de datos")

    # Metodos
    def conectar(self):
        try:
            self.__connection = conector.connect(**self.__mybd)
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def desconectar(self):
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()

    def cursor(self, dictionary=True):
        if self.__connection:
            return self.__connection.cursor(dictionary=dictionary)
        return None
    
    def show_tables(self):
        print("Mostrando tablas")
        try:
            self.__cursor.execute('show tables')
            for i in self.__cursor.fetchall():
                print(i)
        except:
            print("No te encuentras en una base de datos, imposible mostrar tablas")

    def show_databases(self):
        self.__cursor.execute('show databases')
        for i in self.__cursor.fetchall():
            print(i)

    def show_columns(self, table):
        resultado = self.execute(f'desc {table}')
        for i in resultado:
            print(i)


