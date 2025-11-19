from config.db_settings import BaseDeDatos
from repositories_crud.EquipamientoRepository import EquipamentoRepository 
from models.Equipamiento import Equipamiento as Equpo

class EquipamentoService:
    # Constructor 
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.equipamento_repository = EquipamentoRepository(self.db)

    # Metodos
    def registrar_equipamento(self, numEquipa, nombre, descripcion, costoRenta, stock, tipo_equipa, esta_equipa = "DISPO"):
        if not numEquipa or not nombre or not descripcion or not costoRenta or not stock or not esta_equipa or not tipo_equipa:
            print("Los campos no permiten nulos")
            return False

        equipamento = Equpo(numEquipa, nombre, descripcion, costoRenta, stock, esta_equipa, tipo_equipa)
        return self.equipamento_repository.crear_equipamiento(equipamento)


    def listar_equipamentos(self):
        print("Equipamentos registrados:")
        equipamentos = self.equipamento_repository.listar_equipamiento()

        for equipamento in equipamentos:
            print(f"{equipamento['numEquioa']}\t {equipamento['nombre']}\t {equipamento['costoRenta']}\t {equipamento['descripcion']}")

    
    def listar_equipamento_descripcion(self): # Pa checar por lo mismo de q las descripciones son largitas
        print("Equipamentos con descripcion:")
        equipamentos = self.equipamento_repository.listar_equipamiento()

        for equipamento in equipamentos:
            print(f"{equipamento['numEquioa']}\t {equipamento['nombre']}\t {equipamento['descripcion']}")