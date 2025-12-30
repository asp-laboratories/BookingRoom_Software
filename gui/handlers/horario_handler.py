from datetime import datetime, date, timedelta
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush

class HorarioHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion # Assuming the new view will be part of the main navigation
        self.reservacion_service = self.main_window.reservacion
        self.salon_service = self.main_window.salon # Assuming salon service is available on main_window

        # This handler will manage a new 'horario_view' widget
        # The main window needs to instantiate it, e.g., self.horario_view = HorarioView()
        # For now, we assume self.view is this widget.
        self.view = self.main_window.horario_view 

        self.fechas = []
        self.horas = []
        
        # Connect signals from the new UI
        self.view.btnActualizar.clicked.connect(self.actualizar_vista_horario)
        
        self.configurar_tabla_horario()
        self.cargar_salones()
        
        print("✅ HorarioHandler iniciado")

    def cargar_salones(self):
        """
        Carga los salones disponibles en el QComboBox.
        """
        try:
            self.view.comboSalon.clear()
            self.view.comboSalon.addItem("Todos los Salones", None)
            salones = self.salon_service.listar_salones()
            if salones:
                for salon in salones:
                    self.view.comboSalon.addItem(salon["nombre"], salon["numSalon"])
        except Exception as e:
            QMessageBox.critical(self.view, "Error de Carga", f"No se pudieron cargar los salones: {e}")

    def configurar_tabla_horario(self):
        """
        Configura la estructura inicial de la tabla del horario (filas de horas, columnas de días).
        """
        print("Configurando tabla de horario...")
        # Time slots from 7:00 to 22:00 in 30-min intervals
        self.horas = []
        # Horas de 7am a 10pm en intervalos de 30 minutos
        for hora in range(7, 22):  # 19, 20, 21
            self.horas.append(f"{hora:02d}:00")
            self.horas.append(f"{hora:02d}:30")
        self.horas.append("22:00")
        
        self.view.tableHorario.setRowCount(len(self.horas))
        self.view.tableHorario.setColumnCount(7 + 1) # 7 days + 1 hour column

        # Fill hour column
        for i, hora in enumerate(self.horas):
            item = QTableWidgetItem(hora)
            item.setBackground(QColor(240, 240, 240))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.view.tableHorario.setItem(i, 0, item)
        
        self.view.dateInicio.setDate(QDate.currentDate())
        self.actualizar_vista_horario() # Initial load

    def actualizar_vista_horario(self):
        """
        Función principal que se dispara para refrescar todo el horario.
        Obtiene fechas, datos de la BD y renderiza la tabla.
        """
        print("Actualizando vista de horario...")
        
        # 1. Update dates based on QDateEdit
        fecha_inicio = self.view.dateInicio.date().toPyDate()
        self.fechas = [fecha_inicio + timedelta(days=i) for i in range(7)]
        
        headers = ["Hora"] + [f"{f.strftime('%a')}\n{f.strftime('%d/%m')}" for f in self.fechas]
        self.view.tableHorario.setHorizontalHeaderLabels(headers)

        # 2. Fetch data from DB for the date range
        start_date_str = self.fechas[0].strftime('%Y-%m-%d')
        end_date_str = self.fechas[-1].strftime('%Y-%m-%d')
        todas_las_reservaciones = self.reservacion_service.listar_reservaciones_en_rango(start_date_str, end_date_str)
        
        if todas_las_reservaciones is None:
            QMessageBox.critical(self.view, "Error de Base de Datos", "No se pudieron obtener las reservaciones.")
            todas_las_reservaciones = []

        # 3. Filter by salon
        salon_seleccionado = self.view.comboSalon.currentText()
        reservaciones_filtradas = []
        if salon_seleccionado == "Todos los Salones":
            reservaciones_filtradas = todas_las_reservaciones
        else:
            reservaciones_filtradas = [r for r in todas_las_reservaciones if r['nombre_salon'] == salon_seleccionado]

        # 4. Render events
        self.renderizar_eventos(reservaciones_filtradas)

    def renderizar_eventos(self, eventos):
        """
        Limpia la tabla y dibuja los eventos proporcionados.
        """
        print(f"Renderizando {len(eventos)} eventos...")
        
        # Clear table (except hour column)
        for r in range(self.view.tableHorario.rowCount()):
            for c in range(1, self.view.tableHorario.columnCount()):
                self.view.tableHorario.setItem(r, c, None)
        
        # Detect conflicts before rendering
        eventos_procesados, conflictos = self.detectar_conflictos(eventos)

        # Render non-conflicting events
        for evento in eventos_procesados:
            self.marcar_evento(evento, conflict=False)
            
        # Render conflicting events
        for conflicto in conflictos:
            self.marcar_evento(conflicto, conflict=True)

    def detectar_conflictos(self, eventos):
        """
        Toma una lista de eventos y devuelve dos listas: 
        una con eventos sin conflicto y otra con eventos en conflicto.
        """
        eventos.sort(key=lambda x: (x.get('fechaEvento'), x.get('horaInicio')))
        
        conflictos = set()
        eventos_vistos = []

        for i in range(len(eventos)):
            for j in range(i + 1, len(eventos)):
                e1 = eventos[i]
                e2 = eventos[j] 
                
                # Check for overlap only if they are for the same room
                if e1.get('nombre_salon') == e2.get('nombre_salon') and e1.get('fechaEvento') == e2.get('fechaEvento'):
                    # (StartA < EndB) and (StartB < EndA)
                    if e1.get('horaInicio') < e2.get('horaFin') and e2.get('horaInicio') < e1.get('horaFin'):
                        conflictos.add(e1['numReser'])
                        conflictos.add(e2['numReser'])

        eventos_sin_conflicto = [e for e in eventos if e['numReser'] not in conflictos]
        eventos_con_conflicto = [e for e in eventos if e['numReser'] in conflictos]
        
        return eventos_sin_conflicto, eventos_con_conflicto


    def marcar_evento(self, evento, conflict=False):
        """
        Dibuja un único evento en la tabla.
        """
        try:
            # Convert date str from DB to date object if necessary
            fecha_evento = evento['fechaEvento']
            if isinstance(fecha_evento, str):
                fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%d').date()

            # Find column for the event's date
            columna = self.fechas.index(fecha_evento) + 1
            
            # Find start and end rows
            # This logic requires start/end times to match the `self.horas` list perfectly
            fila_inicio = self.horas.index(evento['horaInicio'])
            fila_fin = self.horas.index(evento['horaFin'])
            
            # Draw the event block
            for fila in range(fila_inicio, fila_fin):
                texto = f"{evento['descripEvento']}\n(#{evento['numReser']})"
                item = QTableWidgetItem(texto)
                
                if conflict:
                    item.setBackground(QBrush(QColor(220, 50, 50))) # Red for conflict
                else:
                    item.setBackground(QBrush(QColor(100, 150, 255)))  # Blue for normal

                item.setForeground(QBrush(QColor(255, 255, 255)))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setData(Qt.ItemDataRole.UserRole, evento['numReser'])
                
                self.view.tableHorario.setItem(fila, columna, item)
                
        except (ValueError, IndexError) as e:
            # Error if date is not in the current view or time is not in the list
            print(f"⚠️ No se pudo marcar el evento #{evento.get('numReser')}: {e}")
