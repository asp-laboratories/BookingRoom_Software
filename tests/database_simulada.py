# Simulación de base de datos en memoria
class DatabaseSimulada:
    def __init__(self):
        self.eventos = {}
        self.contador_id = 1
    
    def agregar_evento(self, nombre, fecha, hora_inicio, hora_fin):
        """Agregar evento a la base de datos simulada"""
        evento = {
            'id': self.contador_id,
            'nombre': nombre,
            'fecha': fecha,  # Objeto date
            'hora_inicio': hora_inicio,  # String "HH:MM"
            'hora_fin': hora_fin,  # String "HH:MM"
            'activo': True
        }
        
        self.eventos[self.contador_id] = evento
        self.contador_id += 1
        return evento
    
    def obtener_eventos_por_fecha(self, fecha):
        """Obtener eventos para una fecha específica"""
        eventos_fecha = []
        for evento in self.eventos.values():
            if evento['fecha'] == fecha and evento['activo']:
                eventos_fecha.append(evento)
        return eventos_fecha
    
    def obtener_todos_eventos(self):
        """Obtener todos los eventos activos"""
        return [evento for evento in self.eventos.values() if evento['activo']]
    
    def obtener_evento_por_id(self, evento_id):
        """Obtener evento por ID"""
        return self.eventos.get(evento_id)
    
    def eliminar_evento(self, evento_id):
        """Eliminar evento (marcar como inactivo)"""
        if evento_id in self.eventos:
            self.eventos[evento_id]['activo'] = False
            return True
        return False
    
    def limpiar_base_datos(self):
        """Limpiar toda la base de datos"""
        self.eventos.clear()
        self.contador_id = 1

# Instancia global de la base de datos simulada
db = DatabaseSimulada()
