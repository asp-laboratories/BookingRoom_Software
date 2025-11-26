from config.db_settings import BaseDeDatos
from repositories_crud.EquipamientoRepository import EquipamentoRepository 
from models.Equipamiento import Equipamiento as Equpo
from repositories_crud.TipoEquipamientoRepository import TipoEquipaRepository

class EquipamentoService:
    # Constructor 
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.equipamento_repository = EquipamentoRepository(self.db)
        self.tipo_equipamiento = TipoEquipaRepository(self.db)

    # Metodos
    def registrar_equipamento(self, nombre, descripcion, costoRenta, stock, tipo_equipa, esta_equipa = "DISPO"):
        if  not nombre or not descripcion or not costoRenta or not stock or not esta_equipa or not tipo_equipa:
            print("Los campos no permiten nulos")
            return False
        descripcionte = self.tipo_equipamiento.descripcion_de_tipo(tipo_equipa)
        equipamento = Equpo(nombre, descripcion, costoRenta, stock, esta_equipa, descripcionte.codigoTiEquipa)
        return self.equipamento_repository.crear_equipamiento(equipamento)


    def listar_equipamentos(self):
        print("Equipamentos registrados:")
        equipamentos = self.equipamento_repository.listar_equipamiento()

        for equipamento in equipamentos:
            print(f"{equipamento['numEquipa']}\t {equipamento['nombre']}\t {equipamento['costoRenta']}\t {equipamento['descripcion']}")

    
    def listar_equipamento_descripcion(self): 
        print("Equipamentos con descripcion:")
        equipamentos = self.equipamento_repository.listar_equipamiento()

        for equipamento in equipamentos:
            print(f"{equipamento['numEquipa']}\t {equipamento['nombre']}\t {equipamento['descripcion']}")
    
    def actualizar_equipamento(self, numEquipa, nombre):
        self.equipamento_repository.actualizar_equipamiento(numEquipa,nombre)
    
    def aliminar_equipamento(self,numEquipa):
        self.equipamento_repository.eliminar_equipamiento(numEquipa)