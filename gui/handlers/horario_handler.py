from datetime import datetime, date, timedelta
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush

class HorarioHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.view = self.main_window.navegacion  # La vista ahora es la UI principal de navegación
        self.reservacion_service = self.main_window.reservacion
        self.salon_service = self.main_window.salon

        self.fechas = []
        self.horas = []
        
        # Las conexiones de señales se moverán a admin_screen.py
        
        self.configurar_tabla_horario()
        self.cargar_salones()
        
        print("✅ HorarioHandler iniciado y configurado.")

    def cargar_salones(self):
        """
        Carga los salones disponibles en el QComboBox 'comboSalonHorario'.
        """
        try:
            self.view.comboSalonHorario.clear()
            self.view.comboSalonHorario.addItem("Todos los Salones", None)
            salones = self.salon_service.listar_salones() 
            if salones:
                for salon in salones:
                    # Usamos acceso por clave de diccionario y 'numSalon' como ID
                    self.view.comboSalonHorario.addItem(salon['nombre'], salon['numSalon'])
        except Exception as e:
            QMessageBox.critical(self.view, "Error de Carga", f"No se pudieron cargar los salones: {e}")

    def configurar_tabla_horario(self):
        """
        Configura la estructura inicial de la tabla del horario (filas de horas, columnas de días).
        """
        print("Configurando tabla de horario...")
        self.horas = [f"{h:02d}:{m:02d}" for h in range(7, 24) for m in (0, 30)]
        
        self.view.scheduleTableHorario.setRowCount(len(self.horas))
        self.view.scheduleTableHorario.setColumnCount(7 + 1) # 7 days + 1 hour column
        
        self.view.scheduleTableHorario.setVerticalHeaderLabels(self.horas)
        self.view.scheduleTableHorario.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view.scheduleTableHorario.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.view.scheduleTableHorario.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.view.dateInicioHorario.setDate(QDate.currentDate())
        self.actualizar_vista_horario() # Initial load

    def actualizar_vista_horario(self):
        """
        Función principal que se dispara para refrescar todo el horario.
        Obtiene fechas, datos de la BD y renderiza la tabla.
        """
        print("Actualizando vista de horario...")
        
        fecha_inicio = self.view.dateInicioHorario.date().toPyDate()
        self.fechas = [fecha_inicio + timedelta(days=i) for i in range(7)]
        
        headers = [f"{f.strftime('%a')}\n{f.strftime('%d/%m')}" for f in self.fechas]
        self.view.scheduleTableHorario.setHorizontalHeaderLabels(headers)

        todas_las_reservaciones = self.reservacion_service.obtener_reservaciones_por_semana(fecha_inicio)
        
        if todas_las_reservaciones is None:
            QMessageBox.critical(self.view, "Error de Base de Datos", "No se pudieron obtener las reservaciones.")
            todas_las_reservaciones = []

        salon_id_seleccionado = self.view.comboSalonHorario.currentData()
        reservaciones_filtradas = []
        if salon_id_seleccionado is None or salon_id_seleccionado == -1:
             reservaciones_filtradas = todas_las_reservaciones
        else:
            reservaciones_filtradas = [r for r in todas_las_reservaciones if r.id_salon == salon_id_seleccionado]

        self.renderizar_eventos(reservaciones_filtradas)

    def renderizar_eventos(self, eventos):
        """
        Limpia la tabla y dibuja los eventos proporcionados.
        """
        print(f"Renderizando {len(eventos)} eventos...")
        
        self.view.scheduleTableHorario.clearContents()

        for evento in eventos:
            self.marcar_evento(evento)

    def marcar_evento(self, evento):
        """
        Dibuja un único evento en la tabla.
        """
        try:
            fecha_evento = evento.fecha_reser
            if isinstance(fecha_evento, str):
                fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%d').date()

            if fecha_evento not in self.fechas: return

            columna = self.fechas.index(fecha_evento)
            
            hora_inicio_str = evento.hora_inicio
            hora_fin_str = evento.hora_fin

            fila_inicio = self.horas.index(hora_inicio_str)
            fila_fin = self.horas.index(hora_fin_str)
            
            span = fila_fin - fila_inicio
            self.view.scheduleTableHorario.setSpan(fila_inicio, columna, span, 1)

            texto = f"{evento.evento}\nSalón: {evento.nombre_salon}"
            item = QTableWidgetItem(texto)
            
            item.setBackground(QBrush(QColor(255, 127, 80))) # Color coral/salmón
            item.setForeground(QBrush(QColor(255, 255, 255)))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item.setData(Qt.ItemDataRole.UserRole, evento.id_reservacion)
            
            self.view.scheduleTableHorario.setItem(fila_inicio, columna, item)
                
        except (ValueError, IndexError) as e:
            print(f"⚠️ No se pudo marcar el evento #{evento.id_reservacion} (Fecha: {evento.fecha_reser}, Hora Inicio: {evento.hora_inicio}, Hora Fin: {evento.hora_fin}): {e}")

    def avanzar_semana(self):
        """
        Avanza la fecha de inicio del calendario en 7 días.
        """
        fecha_actual = self.view.dateInicioHorario.date()
        self.view.dateInicioHorario.setDate(fecha_actual.addDays(7))

    def retroceder_semana(self):
        """
        Retrocede la fecha de inicio del calendario en 7 días.
        """
        fecha_actual = self.view.dateInicioHorario.date()
        self.view.dateInicioHorario.setDate(fecha_actual.addDays(-7))
