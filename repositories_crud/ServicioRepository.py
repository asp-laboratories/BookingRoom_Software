from models.Servicios import Servicio
# Servicio Repository o CRUD para la tabla de servicios - Lo que se hace en este archivo son las operaciones de la base de datos, por ejemplo las consultas que conocemos
# apareceran aqui tales como INSERT, SELECT, UPDATE y DELETE.
class ServicioRepository:
    def __init__(self, db_configuracion):
        self.db = db_configuracion # En esta sentencia se pasa un objeto que es mandado desde el archivo ServicioService, basicamente es la manera en la cual 
        #las operaciones podran ser exitosas por que aqui se esta guardando la configuracion de la base de datos.

    def crear_servicio(self, servicio): # Para insertar los datos de un servicio a la base de datos se utiliza, una funcion en la cual contendra un parametro que 
        #se espera que sea un objeto.
        if not self.db.conectar(): # Si la conexion a la base de datos no funciona devolvera False, mediante la propiedades db que es una instancia de un clase, recordar
            #composicion, se puede acceder a la configuracion de la base de datos, si la conexion existe entonces procedera con el codigo, ejecutando el try.
            return False

        try: #Intentamos ejecutar el bloque try.
            cursor = self.db.cursor() #Generamos un cursor para poder hacer las consultas de la base de datos, accedemos al cursor mediante la instancia que es una propiedad
            #de esta clase, guardamos en la variable cursor el resultado de db.cursor().
            cursor.execute("""
                INSERT INTO servicio (nombre, descripcion, costoRenta, tipo_servicio)
                VALUES ( %s, %s, %s, %s)
            """, (servicio.nombre, servicio.descripcion, servicio.costo_renta, servicio.tipo_servicio)) #mediante la variable cursor podemos hacer
            #uso de las diferentes funcionalidades que ofrece execute es una de ellas, estas caracteristicas provienen del importe de mysql-connector. Para insertar los 
            # valores en la tabla de la base de datos se ponen los campos de la tabla y en values %s que tomara los valores entre parentesis. Los valores entre parentesis
            # son los valores que se ingresaran, en este caso podemos ver que el parametro actuara como objeto, entonces mediante el . podemos acceder lo que contiene
            #ese objeto y eso es lo que se enviara a la tabla.
    
            self.db.connection.commit() #Metodo de la base de datos que es necesario para que el insert no se pierda y sea exitoso.
            print("Se añadio un de servicio") #mensaje de confirmacion de que todo salio correcto.
            return True #Retornar True si todo salio como se esperaba.
        except Exception as error: #Si el bloque de codigo en try detecta un error, esta excepcion lo capturara.
            print(f"Error al crear un servicio: {error}") #Mediante el alias mostramos en pantalla el error.
            return False #Retornamos False.
        finally:
            cursor.close() # Cerramos tanto el cursor como la base de datos ESTO SIEMPRE SE HACE EN CADA CONSULTA PARA NO TENER ERRORES, en la sentencia finally que siempre
            #ejecutara.
            self.db.desconectar()

    def listar_servicio(self):#Metodo para traer todos los datos de una tabla.
        if not self.db.conectar(): # La misma explicacion la conexion de arriba pero en esta ocasion retorna None, significa que si no pudo conectarse devuelva NADA.
            return False
        try:
            cursor = self.db.cursor(dictionary=True) #Obtenemos el cursor para poder hacer consultas, pero convertimos el cursor a diccioario.
            cursor.execute("SELECT * FROM servicio") #Hacemos la consulta para traer todos los servicios.
            resultados = cursor.fetchall() #Guardamos en una variable cursor.fetchall() que basicamente significa que trae todos los resultados existe otro que es
            #cursor.fetchone() que solo trae una solo fila es aplicable para casos donde se utilize un where.

        except Exception as error: # Si hubo un error, aparecera este mensaje junto con el motivo del error.
            print(f"Error al listar los servicios: {error}") 
        finally:
            cursor.close() # Cerramos el cursor y la base de datos.
            self.db.desconectar()
        return resultados # Retornamos el resultado, tenemos que recordar que es un diccionario, importante.


    def listar_servicio_buscar(self, nombre):#Metodo para traer todos los datos de una tabla.
        if not self.db.conectar(): # La misma explicacion la conexion de arriba pero en esta ocasion retorna None, significa que si no pudo conectarse devuelva NADA.
            return False
        try:
            cursor = self.db.cursor(dictionary=True) #Obtenemos el cursor para poder hacer consultas, pero convertimos el cursor a diccioario.
            cursor.execute(f"SELECT * FROM servicio WHERE nombre LIKE '%{nombre}%'") #Hacemos la consulta para traer todos los servicios.
            resultados = cursor.fetchall() #Guardamos en una variable cursor.fetchall() que basicamente significa que trae todos los resultados existe otro que es
            #cursor.fetchone() que solo trae una solo fila es aplicable para casos donde se utilize un where.

        except Exception as error: # Si hubo un error, aparecera este mensaje junto con el motivo del error.
            print(f"Error al listar los servicios: {error}") 
        finally:
            cursor.close() # Cerramos el cursor y la base de datos.
            self.db.desconectar()
        return resultados # Retornamos el resultado, tenemos que recordar que es un diccionario, importante.

    def actualizar_servicios(self, campo, numServicio, valor):
        if not self.db.conectar():
            return False
        CAMPOS = {
            "Nombre": "nombre",
            "Costo renta": "costoRenta",
            "Tipo de servicio": "tipo_servicio",
            "Descripcion" : "descripcion"
        }
        
        if campo not in CAMPOS:
            print("Error: Nombre de campo no válido o no permitido para actualización.")
            return False
        campo_act = CAMPOS[campo]

        try:
           cursor = self.db.cursor(dictionary=True)
           cursor.execute(f"""
                UPDATE servicio
                SET {campo_act} = %s 
                WHERE numServicio =%s
           """,(valor, numServicio, ))
           self.db.connection.commit()
           print("Servicio actualizado correctamente")
           return True
        except Exception as error:
            print(f"Error al actualizar: {error}")
        finally:
            cursor.close()
            self.db.desconectar()




    def eliminar_servicios(self, numServicio):
        if not self.db.conectar():
            return None
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                DELETE FROM servicio 
                WHERE numServicio = %s
            """, (numServicio,))
            self.db.connection.commit()
            print("Servicio eliminado correctamente")
        except Exception as error:
            print(f"Error al eliminar servicio: {error}")
        finally:
            cursor.close()
            self.db.desconectar()


    
    def obtener_servicios_inner(self): #Metodo para traer mucha informacion en un inner join.
        if not self.db.conectar():
            return None # Misma explicacion de arriba.
        
        try:
            cursor = self.db.cursor(dictionary=True) # Misma explicacion de arriba.
            
            cursor.execute("""
                SELECT 
                    s.numServicio as numServicio,
                    s.nombre as servicio,
                    s.descripcion as descripcion, 
                    s.costoRenta as costoRenta,
                    s.tipo_servicio as ts,
                    t.descripcion as tipo  
                FROM servicio as s
                INNER JOIN tipo_servicio as t  ON s.tipo_servicio = t.codigoTiSer
            """)# Sentencia conocida, inner join con integridad referencial.
            
            results = cursor.fetchall() # Misma explicacion de arriba, recibimos un diccionario.
            servicios = [] #Creamos un arreglo para solo guardar la informacion que nos sea de utilidad.
            
            for row in results: # Mecanica para poder meter los datos del diccionario en un objeto, hay que pensar como si el llamado de la clase este en posicion
                #horizontal, con row accemos a la informacion que nos dio results, entre los corchetes intentara encontrar un valor igual, si nos damos cuenta entre 
                 # estos corchetos se pone el alias asignado a la hora de hacer el inner join.
                servicio = Servicio(
                    nombre=row['servicio'],
                    descripcion=row['descripcion'],
                    costo_renta=row['costoRenta'],
                    tipo_servicio=row['ts']
                ) #Cada propiedad de la clase esta igualado a los rows, lo que significa que las propiedades guardaran la informacion que contenga ese row, en este caso los
                # datos del servicio.              
                servicio.tipo_nombre = row['tipo']  # la clase Servicio tiene una propiedad que esta por fuera del constructor es decir que no se requiere en el llenado
                #y es por que esta por fuera a la hora de la creacion de la instancia, si no hay intancia creada esto no va funcionar por obvias razones.
                servicios.append(servicio)#Recordando el arreglo de arriba, guardamos el objeto/intancia servicio.
            
            return servicios #Enviamos de regreso el arreglo de servicios.
            
        except Exception as e:
            print(f"Error: {e}") #Si encontramos un error, enviar None
            return None
        finally:
            self.db.desconectar() #desconectar base de datos y cursor.

    def obtener_num_servicio(self, nombre):
        if not self.db.conectar():
            return None
        
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT numServicio FROM servicio WHERE nombre like %s", (f"%{nombre}%",))
            numServicio = cursor.fetchone()
            print(numServicio)
            return numServicio

        except Exception as error:
            print(f"Error al mostrar el numero del servicio: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()
        
        
    def conjunto_servicios(self, descripcion):
        if not self.db.conectar():
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT
                tser.descripcion as tipo_servicio,
                ser.nombre as servicio,
                ser.descripcion as descservicio,
                ser.costoRenta as costo_renta
                FROM servicio as ser
                INNER JOIN tipo_servicio as tser on ser.tipo_servicio = tser.codigoTiSer
                WHERE tser.codigoTiSer = %s
            """, (descripcion,))
            resultado = cursor.fetchall()
            return resultado
        except Exception as error:
            print(f"Error al mostrar al mostrar conjunto: {error}")
            return None
        
        finally:
            cursor.close()
            self.db.desconectar()






    # def servicio_mismo_tipo(self, descripcion):
    #     if not self.db.conectar():
    #         return None 
    #     try:
    #         cursor = self.db.cursor()
    #         cursor.execute("""
    #             SELECT
    #             tser.descripcion as tipo_servicio,
    #             ser.nombre as servicio,
    #             ser.descripcion as descservicio,
    #             ser.costoRenta
    #             FROM servicio as ser
    #             INNER JOIN tipo_servicio as tser on ser.tipo_servicio = tser.codigoTiSer
    #             WHERE tser.codigoTiSer = %s """,(f"%{descripcion}%",))
    #         numServicio = cursor.fetchall()
    #
    #         return numServicio
    #     except Exception as error:
    #         print(f"Error al mostrar el numero del servicio: {error}")
    #         return None
    #     
    #     finally:
    #         cursor.close()
    #         self.db.desconectar()
        

