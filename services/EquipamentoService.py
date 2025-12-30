from config.db_settings import BaseDeDatos
from repositories_crud.EquipamientoRepository import EquipamentoRepository
from models.Equipamiento import Equipamiento as Equpo
from repositories_crud.EstadoEquipaRepository import EstadoEquipaRepository
from repositories_crud.TipoEquipamientoRepository import TipoEquipaRepository
from repositories_crud.InventarioEquipaRepository import InventarioEquipaRepository


class EquipamentoService:
    # Constructor
    def __init__(self):
        self.db = BaseDeDatos(database="BookingRoomLocal")
        self.equipamento_repository = EquipamentoRepository(self.db)
        self.tipo_equipamiento = TipoEquipaRepository(self.db)
        self.estado = EstadoEquipaRepository(self.db)
        self.InventarioEquipamientoRepository = InventarioEquipaRepository(self.db)

    # Metodos
    def registrar_equipamento(
        self, nombre, descripcion, costoRenta, stock, codigo_tipo_equipa, esta_equipa="DISPO"
    ):
        if (
            not nombre
            or not descripcion
            or not costoRenta
            or not stock
            or not esta_equipa
            or not codigo_tipo_equipa
        ):
            print("Los campos no permiten nulos")
            return False
        
        equipamento = Equpo(
            nombre,
            descripcion,
            costoRenta,
            stock,
            esta_equipa,
            codigo_tipo_equipa,
        )
        return self.equipamento_repository.crear_equipamiento(equipamento)

    def listar_equipamentos_informacion(self, numEquipa):
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
            print(
                f"{equipamento['numEquipa']}\t {equipamento['nombre']}\t {equipamento['descripcion']}"
            )

    def actualizar_equipamento(self, campo, numEquipa, valor):
        return self.equipamento_repository.actualizar_equipamientos(
            campo, numEquipa, valor
        )

    def aliminar_equipamento(self, numEquipa):
        self.equipamento_repository.eliminar_equipamiento(numEquipa)

    def obtener_equipa_estado(self, esta_equipa):
        print("Listando mobiliarios por su estado")
        esta_equipa = self.estado.obtener_codigo_estado(esta_equipa)
        resultado = self.estado.listar_equipa_por_estado(esta_equipa["codigoEquipa"])
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
        return codigoEquipa["codigoEquipa"]

    def obtener_codigo_equipamiento(self, equipamiento):
        numEquipa = self.equipamento_repository.obtener_num_equipa(equipamiento)
        if not numEquipa:
            print("Equipamiento no valido o no existente")
            return None
        return numEquipa["numEquipa"]

    def actualizar_estado_equipamiento(
        self, num_equipo: int, estado_origen: str, nuevo_estado: str, cantidad: int
    ):
        """
        Actualiza el estado de una cantidad de equipamiento, moviéndola de un estado a otro.

        Args:
            num_equipo (int): El ID del equipamiento a actualizar.
            estado_origen (str): La descripción del estado original (ej. "DISPO").
            nuevo_estado (str): La descripción del nuevo estado (ej. "EN REPARACION").
            cantidad (int): La cantidad de unidades a mover.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            # Convertir descripciones de estado a códigos de estado
            codigo_estado_origen = self.obtener_codig_estado(estado_origen)
            codigo_nuevo_estado = self.obtener_codig_estado(nuevo_estado)

            if not codigo_estado_origen or not codigo_nuevo_estado:
                print(f"Error: Uno o ambos estados ('{estado_origen}', '{nuevo_estado}') son inválidos.")
                return False

            # El ID del equipamiento (num_equipo) ya es un entero, no se necesita lookup.

            # Llamar al repositorio con los códigos de estado y el ID del equipamiento
            resultado = self.InventarioEquipamientoRepository.actualizar_estado_equipamiento(
                num_equipo, codigo_estado_origen, codigo_nuevo_estado, cantidad
            )
            
            return resultado

        except Exception as e:
            print(f"Error en la capa de servicio al actualizar estado de equipamiento: {e}")
            return False

    def obtener_cantidad_en_estado(self, num_equipo: int, estado_descripcion: str):
        """
        Obtiene la cantidad de un equipo específico en un estado particular.

        Args:
            num_equipo (int): El ID del equipamiento.
            estado_descripcion (str): La descripción del estado (ej. "DISPO").

        Returns:
            int: La cantidad de unidades del equipo en ese estado, o 0 si no se encuentra.
        """
        try:
            codigo_estado = self.obtener_codig_estado(estado_descripcion)
            if not codigo_estado:
                print(f"Estado '{estado_descripcion}' no válido.")
                return 0
            
            cantidad = self.InventarioEquipamientoRepository.obtener_cantidad_por_equipo_y_estado(
                num_equipo, codigo_estado
            )
            return cantidad
        except Exception as e:
            print(f"Error al obtener cantidad en estado: {e}")
            return 0

    def listar_equipamientos_reser(self, numReser):
        return self.equipamento_repository.listar_equipamientos_reser(numReser)

    def comprobar_stock(self, numEquipa, cantidad):
        disponibles = self.equipamento_repository.obtener_disponibles(numEquipa)

        if cantidad < disponibles["cantidad"]:
            print("No hay suficientes equipamientos disponibles")
            return False
        else:
            print("Suficientes equipamientos disponibles")
            return True

    def eliminar_registro(self, numEquipa):
        return self.equipamento_repository.eliminar_registro_equipamiento(numEquipa)

    def listar_equipamiento_tipo(self, descripcion):
        return self.tipo_equipamiento.conjunto_equipamientos(descripcion)

    def listar_estados(self):
        return self.estado.listar_estados()
