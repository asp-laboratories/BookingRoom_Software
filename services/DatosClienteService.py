from config.db_settings import BaseDeDatos
from models.DatosCliente import DatosCliente
from repositories_crud.DatosClientesRepository import DatosClientesRepository


class DatosClienteService:
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.cliente_repository = DatosClientesRepository(self.db)
       
    def registrar_clientes(self, rfc, contNombre, contPriApellido, contSegApellido , nombreFiscal, email, dirColonia, dirCalle, dirNumero,tipo_cliente):
        cliente = DatosCliente(rfc, contNombre, contPriApellido, contSegApellido , nombreFiscal, email, dirColonia, dirCalle, dirNumero,tipo_cliente)
        return self.cliente_repository.crear_cliente(cliente)
    
    def listar_cliente_busqueda(self, rfc):
        return self.cliente_repository.listar_cliente_busqueda(rfc)
    def listar_clientes(self):
        print("clientes: ")
        cliente = self.cliente_repository.listar_cliente()
        print("RFC:\t Nombre:\t")
        for row in cliente:
            print(f"{row['RFC']}\t {row['contNombre']}")

    def obtener_rfc(self, nombreFiscal):
        rfc = self.cliente_repository.obtener_rfc(nombreFiscal)
        return rfc['rfc']
