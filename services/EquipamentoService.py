from config.db_settings import BaseDeDatos
from repositories_crud.EquipamientoRepository import EquipamentoRepository 
from models.Equipamiento import Equipamiento as Equpo
from repositories_crud.EstadoEquipaRepository import EstadoEquipaRepository
from repositories_crud.TipoEquipamientoRepository import TipoEquipaRepository
from repositories_crud.EstadoEquipaRepository import EstadoEquipaRepository
from repositories_crud.InventarioEquipaRepository import InventarioEquipaRepository

class EquipamentoService:
    # Constructor 
    def __init__(self):
        self.db = BaseDeDatos(database='BookingRoomLocal')
        self.equipamento_repository = EquipamentoRepository(self.db)
        self.tipo_equipamiento = TipoEquipaRepository(self.db)
        self.estado = EstadoEquipaRepository(self.db)
        self.InventarioEquipamientoRepository = InventarioEquipaRepository(self.db)

    # Metodos
    def registrar_equipamento(self, nombre, descripcion, costoRenta, stock, tipo_equipa, esta_equipa = "DISPO"):
        if  not nombre or not descripcion or not costoRenta or not stock or not esta_equipa or not tipo_equipa:
            print("Los campos no permiten nulos")
            return False
        descripcionte = self.tipo_equipamiento.descripcion_de_tipo(tipo_equipa)
        equipamento = Equpo(nombre, descripcion, costoRenta, stock, esta_equipa, descripcionte.codigoTiEquipa)
        return self.equipamento_repository.crear_equipamiento(equipamento)

    def listar_equipamentos_informacion(self,numEquipa):
        print("Equipamentos registrados:")
        return self.equipamento_repository.listar_equipamiento_informacion(numEquipa)

    def listar_equipamentos(self):
        print("Equipamentos registrados:")
        return self.equipamento_repository.listar_equipamiento()

        # for equipamento in equipamentos:
        #     print(f"{equipamento['numEquipa']}\t {equipamento['nombre']}\t {equipamento['costoRenta']}\t {equipamento['descripcion']}")

    
    def listar_equipamento_descripcion(self): 
        print("Equipamentos con descripcion:")
        equipamentos = self.equipamento_repository.listar_equipamiento()

        for equipamento in equipamentos:
            print(f"{equipamento['numEquipa']}\t {equipamento['nombre']}\t {equipamento['descripcion']}")
    
    def actualizar_equipamento(self, campo, numEquipa, valor):
        self.equipamento_repository.actualizar_equipamientos(campo,numEquipa,valor)
    
    def aliminar_equipamento(self,numEquipa):
        self.equipamento_repository.eliminar_equipamiento(numEquipa)

    def obtener_equipa_estado(self, esta_equipa):
        print("Listando mobiliarios por su estado")
        esta_equipa = self.estado.obtener_codigo_estado(esta_equipa)
        resultado =  self.estado.listar_equipa_por_estado(esta_equipa['codigoEquipa'])
        return resultado
    
    def actualizar_estado(self, codigoEquipa, descripcion):
        self.estadoEquipaRepository.actualizar_estado_equipa(codigoEquipa, descripcion)

    def eliminar_estado(self, codigoEquipa):
        self.estadoEquipaRepository.eliminar_estado_equipa(codigoEquipa)

    def obtener_codig_estado(self, descripcionEstado):
        codigoEquipa = self.estado.obtener_codigo_estado(descripcionEstado)
        if not codigoEquipa:
            print("Estado de equipamiento no existente")
            return None
        return codigoEquipa['codigoEquipa']
    
    def obtener_codigo_equipamiento(self, equipamiento):
        numEquipa = self.equipamento_repository.obtener_num_equipa(equipamiento)
        if not numEquipa:
            print("Equipamiento no valido o no existente")
            return None
        return numEquipa['numEquipa']

    def actualizar_estado_equipamiento(self, equipamiento, estado_og, new_estado, cantidad):
        estado_og = self.obtener_codig_estado(estado_og)
        new_estado = self.obtener_codig_estado(new_estado)
        print(f"{estado_og} {new_estado} {equipamiento}")
        #equipamiento = self.obtener_codigo_equipamiento(equipamiento)

        if (not estado_og) or (not new_estado) or (not equipamiento):
            print("No procede la actualizacion de estado")
            return False

        self.InventarioEquipamientoRepository.actualizar_estado_equipamiento(equipamiento, estado_og, new_estado, cantidad)
        return True

    def listar_equipamientos_reser(self, numReser):
        return self.equipamento_repository.listar_equipamientos_reser(numReser)
    
    def comprobar_stock(self, numEquipa, cantidad):
        disponibles = self.equipamento_repository.obtener_disponibles(numEquipa)

        if cantidad < disponibles['cantidad']:
            print("No hay suficientes equipamientos disponibles")
            return False
        else:
            print("Suficientes equipamientos disponibles")
            return True

    def eliminar_registro(self,numEquipa):
        return self.equipamento_repository.eliminar_registro_equipamiento(numEquipa)

    def listar_equipamiento_tipo(self, descripcion):
        return self.tipo_equipamiento.conjunto_equipamientos(descripcion)
