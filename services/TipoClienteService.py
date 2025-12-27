from config.db_settings import BaseDeDatos
from repositories_crud.TipoClienteRepository import TipoClienteRepository


class TipoClienteService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database="BookingRoomLocal")
        self.tipoclienteRepository = TipoClienteRepository(self.db)

    # Metodos
    def listar_tipos_cliente(self):
        return self.tipoclienteRepository.listar_tipos_clientes()

    def listar_clientes_por_tipo(self, descripcion):
        codigoCli = self.obtener_codigo_tipo_cliente(descripcion)
        info_clientes = self.tipoclienteRepository.listar_clientes_por_tipo(codigoCli)

        clientes = []

        aux_clientes = []
        for cliente in info_clientes:
            if cliente["contacto"] not in aux_clientes:
                aux_clientes.append(cliente["contacto"])
                clnt = {
                    "nombreFiscal": cliente["nombreFiscal"],
                    "RFC": cliente["RFC"],
                    "tipo_cliente": cliente["descripcion"],
                    "contacto": cliente["contacto"],
                    "email": cliente["email"],
                    "direccion": cliente["direccion"],
                    "telefonos": [],
                }
                clnt["telefonos"].append(cliente["telefono"])

                clientes.append(clnt)

            else:
                for cliente2 in clientes:
                    if cliente2["contacto"] == cliente["contacto"]:
                        cliente2["telefonos"].append(cliente["telefono"])

        return clientes

    def obtener_codigo_tipo_cliente(self, descripcion):
        codigoCli = self.tipoclienteRepository.obtener_codigo_tipo_cliente(descripcion)
        return codigoCli["codigoCli"]
