from config.db_settings import BaseDeDatos
from models.Servicios import Servicio
from repositories_crud.ServicioRepository import ServicioRepository

class ServicioService: #Clase que ayudara a gestionar las operaciones de la base de datos.
    def __init__(self) -> None:
        self.db = BaseDeDatos(database='BookingRoomLocal') #Desde aqui se envia la configuracion de la base de datos a ServicioRepository, en este caso
         # es mi base de datos local, pero cuando se tenga la del servidor, se pondran mas parametros como lo son la contraseña, usuario y otro nombre.
        self.servicio_repository = ServicioRepository(self.db)#Pasamos la propiedad creada arriba, que en realidad es una instancia que contendra toda la informacion,
        # pero ademas de pasar la configuracion tambien creados otra instancia/objeto con el cual nos vamos a poder comunicar con las operaciones de la base de datos.
       
    def registrar_servicio(self, codigoSer, nombre, descripcion, costo_renta, tipo_servicio): #Metodo para registrar un servicio que en tests/test_servicio.py hay un
        #ejemplo en terminal pero esto tambien sirve para la interfaz grafica, para hacer pruebas es recomendable hacerlo en terminal como siempre se ha hecho.
        servicio = Servicio(codigoSer, nombre, descripcion, costo_renta, tipo_servicio) #Mediante los parametros obtenidos creamos un objeto llamando a la clase Servicio en 
        #los imports se muestra de donde viene cada archivo.
        return self.servicio_repository.crear_servicio(servicio) #Opcional retornar ya que con el simple hecho de llamar a la funcion del repository es funcional.

    def listar_servicio(self): #Metodo para listar los datos a pantalla.
        print("Servicios: ")
        servicio = self.servicio_repository.listar_servicio() #Recordando que devuelve un diccionario
        print("Codigo:\t Nombre:\t Descripcion:\t Costo:\t Tipo: ")#\t para tabulacion
        for row in servicio:
            print(f"{row['codigoSer']}\t {row['nombre']}\t {row['descripcion']}\t {row['costoRenta']}\t") #row es como si fuera i de esta manera regresara todo lo que 
            #encuentre de la tabla servicios.

    def listar_servicio_y_tipo(self):
        servicios = self.servicio_repository.obtener_servicios_inner() # Recordando que devuelve un arreglo.
        if servicios: #Si servicios existe entonces:
            for ser in servicios:
                print(f"Informacion de: {ser.nombre}:\n{ser.descripcion}\n{ser.costo_renta}\n{ser.tipo_nombre}") #ser es como si fuera i, solo que ser contiene los
                #objetos que encuentre mediante el . accede a la informacion.

