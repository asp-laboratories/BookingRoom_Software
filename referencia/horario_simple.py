import sys
from datetime import datetime, date, timedelta
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush

from database_simulada import db

class HorarioSimple(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("horario_simple.ui", self)
        
        # Configurar fechas iniciales
        self.fechas = []
        self.configurar_fechas_iniciales()
        
        # Conectar eventos
        self.btnAgregar.clicked.connect(self.agregar_evento)
        self.btnMostrar.clicked.connect(self.mostrar_eventos)
        self.btnLimpiar.clicked.connect(self.limpiar_horario)
        self.btnActualizar.clicked.connect(self.actualizar_fechas)
        
        # Conectar doble clic en celdas
        self.tableHorario.cellDoubleClicked.connect(self.celda_doble_clic)
        
        # Configurar horario
        self.configurar_horario()
        
        print("✅ Horario simple iniciado")
        print("📅 Base de datos simulada lista")
    
    def configurar_fechas_iniciales(self):
        """Configurar fechas iniciales (hoy + 6 días)"""
        hoy = date.today()
        self.fechas = [hoy + timedelta(days=i) for i in range(7)]
        
        # Establecer fecha inicial en el QDateEdit
        self.dateInicio.setDate(QDate.currentDate())
        self.dateEvento.setDate(QDate.currentDate())
    
    def configurar_horario(self):
        """Configurar tabla del horario"""
        # Horas de 7pm a 10pm en intervalos de 30 minutos
        self.horas = []
        for hora in range(7, 22):  # 19, 20, 21
            for minuto in [0, 30]:
                if hora == 21 and minuto == 30:
                    continue  # No incluir 21:30
                self.horas.append(f"{hora:02d}:{minuto:02d}")
        self.horas.append("22:00")  # Agregar 22:00
        
        print(f"🕐 Horas configuradas: {self.horas}")
        
        # Configurar tabla
        self.tableHorario.setRowCount(len(self.horas))
        self.tableHorario.setColumnCount(len(self.fechas) + 1)
        
        # Actualizar encabezados
        self.actualizar_encabezados()
        
        # Llenar columna de horas
        for i, hora in enumerate(self.horas):
            item = QTableWidgetItem(hora)
            item.setBackground(QColor(240, 240, 240))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableHorario.setItem(i, 0, item)
        
        # Cargar eventos existentes
        self.cargar_eventos()
    
    def actualizar_encabezados(self):
        """Actualizar encabezados de la tabla con las fechas"""
        headers = ["Hora"]
        for fecha in self.fechas:
            # Formato: "Lun 15/01"
            dia = fecha.strftime("%a")
            fecha_corta = fecha.strftime("%d/%m")
            headers.append(f"{dia}\n{fecha_corta}")
        
        self.tableHorario.setHorizontalHeaderLabels(headers)
    
    def actualizar_fechas(self):
        """Actualizar las fechas mostradas en el horario"""
        fecha_inicio = self.dateInicio.date().toPyDate()
        self.fechas = [fecha_inicio + timedelta(days=i) for i in range(7)]
        
        print(f"🔄 Actualizando fechas: {[f.strftime('%d/%m') for f in self.fechas]}")
        
        # Limpiar tabla (excepto columna de horas)
        self.limpiar_tabla()
        
        # Actualizar encabezados
        self.actualizar_encabezados()
        
        # Recargar eventos para las nuevas fechas
        self.cargar_eventos()
        
        QMessageBox.information(self, "Éxito", "Fechas actualizadas")
    
    def limpiar_tabla(self):
        """Limpiar la tabla (mantener solo columna de horas)"""
        for fila in range(self.tableHorario.rowCount()):
            for columna in range(1, self.tableHorario.columnCount()):
                self.tableHorario.setItem(fila, columna, QTableWidgetItem(""))
    
    def agregar_evento(self):
        """Agregar nuevo evento"""
        try:
            # Obtener datos
            nombre = self.inputNombre.text().strip()
            fecha = self.dateEvento.date().toPyDate()
            hora_inicio = self.timeInicio.time().toString("HH:mm")
            hora_fin = self.timeFin.time().toString("HH:mm")
            
            print(f"➕ Intentando agregar evento: {nombre} | {fecha} | {hora_inicio}-{hora_fin}")
            
            # Validaciones simples
            if not nombre:
                QMessageBox.warning(self, "Error", "Ingresa un nombre para el evento")
                return
            
            if hora_inicio >= hora_fin:
                QMessageBox.warning(self, "Error", "La hora de fin debe ser mayor a la de inicio")
                return
            
            # Verificar que la fecha esté en el rango mostrado
            if fecha not in self.fechas:
                QMessageBox.warning(self, "Error", 
                                  f"La fecha {fecha.strftime('%d/%m/%Y')} debe estar en el rango mostrado")
                return
            
            # Verificar que las horas estén en el rango
            if hora_inicio not in self.horas or hora_fin not in self.horas:
                QMessageBox.warning(self, "Error", 
                                  f"Las horas deben estar entre 19:00 y 22:00")
                return
            
            # Verificar disponibilidad
            if not self.verificar_disponibilidad(fecha, hora_inicio, hora_fin):
                QMessageBox.warning(self, "Conflicto", 
                                  "Ya hay un evento en ese horario")
                return
            
            # Guardar en base de datos simulada
            evento = db.agregar_evento(nombre, fecha, hora_inicio, hora_fin)
            print(f"✅ Evento guardado en BD: {evento}")
            
            # Actualizar horario
            self.marcar_evento_en_horario(evento)
            
            # Limpiar formulario
            self.inputNombre.clear()
            
            QMessageBox.information(self, "Éxito", 
                                  f"Evento '{nombre}' agregado para {fecha.strftime('%d/%m/%Y')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    
    def verificar_disponibilidad(self, fecha, hora_inicio, hora_fin):
        """Verificar si el horario está disponible"""
        eventos_fecha = ob.obtener_eventos_por_fecha(fecha)
        
        for evento in eventos_fecha:
            # Verificación simple de superposición
            if not (hora_fin <= evento['hora_inicio'] or hora_inicio >= evento['hora_fin']):
                print(f"❌ Conflicto con evento: {evento}")
                return False
        return True
    
    def cargar_eventos(self):
        """Cargar todos los eventos en el horario"""
        todos_eventos = db.obtener_todos_eventos()
        print(f"📂 Cargando {len(todos_eventos)} eventos en el horario")
        
        for evento in todos_eventos:
            if evento['fecha'] in self.fechas:
                print(f"  - Marcando evento: {evento}")
                self.marcar_evento_en_horario(evento)
    
    def marcar_evento_en_horario(self, evento):
        """Marcar un evento en el horario"""
        try:
            # Encontrar posición en la tabla
            fila_inicio = self.horas.index(evento['hora_inicio'])
            fila_fin = self.horas.index(evento['hora_fin'])
            columna = self.fechas.index(evento['fecha']) + 1
            
            print(f"  🎯 Marcando en: fila {fila_inicio}-{fila_fin}, columna {columna}")
            
            # Marcar celdas
            for fila in range(fila_inicio, fila_fin):
                item = QTableWidgetItem(evento['nombre'])
                item.setBackground(QBrush(QColor(100, 150, 255)))  # Azul
                item.setForeground(QBrush(QColor(255, 255, 255)))  # Texto blanco
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Guardar ID del evento para poder identificarlo
                item.setData(Qt.ItemDataRole.UserRole, evento['id'])
                
                self.tableHorario.setItem(fila, columna, item)
                print(f"    ✅ Celda [{fila}, {columna}] marcada: {evento['nombre']}")
                
        except ValueError as e:
            print(f"⚠️ Error marcando evento {evento}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def celda_doble_clic(self, fila, columna):
        """Manejar doble clic en celdas para eliminar eventos"""
        if columna == 0:  # Columna de horas
            return
        
        item = self.tableHorario.item(fila, columna)
        if item and item.data(Qt.ItemDataRole.UserRole):
            evento_id = item.data(Qt.ItemDataRole.UserRole)
            evento = next((e for e in db.obtener_todos_eventos() if e['id'] == evento_id), None)
            
            if evento:
                respuesta = QMessageBox.question(
                    self, "Eliminar Evento", 
                    f"¿Eliminar evento?\n\n"
                    f"📝 {evento['nombre']}\n"
                    f"📅 {evento['fecha'].strftime('%d/%m/%Y')}\n"
                    f"⏰ {evento['hora_inicio']} - {evento['hora_fin']}",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if respuesta == QMessageBox.StandardButton.Yes:
                    db.eliminar_evento(evento_id)
                    self.actualizar_fechas()  # Recargar el horario
                    QMessageBox.information(self, "Éxito", "Evento eliminado")
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HorarioSimple()
    window.show()
    sys.exit(app.exec())
