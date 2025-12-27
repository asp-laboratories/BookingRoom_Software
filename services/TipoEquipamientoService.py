from repositories_crud.TipoEquipamientoRepository import TipoEquipaRepository
from config.db_settings import BaseDeDatos
from models.TipoEquipa import TipoEquipa


class TipoEquipamentoService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database="BookingRoomLocal")
        # self.db = BaseDeDatos(database='BookingRoomLoca')
        self.repository = TipoEquipaRepository(self.db)

    # Metodos
    def registrar_tipo_equipamento(self, codigoTiEquipa, descripcion):
        if not codigoTiEquipa or not descripcion:
            print("Los campos no permiten nulos")
            return False

        tipo_equipa = TipoEquipa(codigoTiEquipa=codigoTiEquipa, descripcion=descripcion)
        return self.repository.crear_tipo_equipamento(tipo_equipa)

    def listar_tipos_equipamentos(self):
        return self.repository.listar_tipo_equipamentos()

    def mostrar_equipamentos_tipo(self, tipo_equipa):
        tipo = self.repository.obtener_equipamentos_de_tipo(tipo_equipa)

        if tipo:
            print(f"-----{tipo}-----")
            print("Servicios:")
            if tipo.equipamientos:
                for equipamiento in tipo.equipamientos:
                    print(f" - {equipamiento.nombre}")
            else:
                print(" No tiene ningun equipamento asignado")
        else:
            print("Tipo de equipamento no encontrado, consulte tipos registrados")
