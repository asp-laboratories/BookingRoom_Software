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

            self.__cursor = self.__mybd.cursor()
            print("Conexion establecida")
        except:
            print("Conexion Fallida a la base de datos")

    # Metodos
    def execute(self, consulta):
        print("Intentando consulta")
        self.__cursor.execute(consulta)
        return self.__cursor.fetchall()
    
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

    def close(self):
        self.__cursor.close()
        self.__mybd.close()
