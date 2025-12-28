from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class TableManager:
    """Gestor simple para crear tablas atractivas"""
    
    @staticmethod
    def create_simple_table(headers, data=None, parent=None):
        """
        Crea una tabla básica y bien estilizada
        
        Args:
            headers: Lista de nombres para las columnas
            data: Lista de listas con los datos (opcional)
            parent: Widget padre (opcional)
        
        Returns:
            QTableWidget configurada y estilizada
        """
        table = QTableWidget(parent)
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # Configuración básica para buena apariencia
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        
        # Estilo limpio y profesional
        table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-size: 13px;
                alternate-background-color: #f5ddb9; 
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f8f9fa;
            }
            QHeaderView::section {
                background-color: #f5ddb9; 
                color: #D18A5B; 
                padding: 10px;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #9b582b; 
                color: #ffffff; 
            }
        """)
        
        # Si hay datos, llenar la tabla
        if data:
            TableManager.fill_table(table, data)
        
        return table
    
    @staticmethod
    def fill_table(table, data):
        """Llena la tabla con datos"""
        if not data:
            TableManager.show_message(table, "No hay datos para mostrar")
            return
        
        table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                table.setItem(row_idx, col_idx, item)
        
        # Ajustar columnas al contenido
        table.resizeColumnsToContents()
        
        # Si alguna columna es muy estrecha, expandirla
        header = table.horizontalHeader()
        for i in range(table.columnCount()):
            if header.sectionSize(i) < 80:  # Si es menor a 80px
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
    
    @staticmethod
    def show_message(table, message, icon="📭"):
        """Muestra un mensaje centrado en la tabla"""
        table.clear()
        table.setRowCount(1)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([''])
        
        item = QTableWidgetItem(f"{icon} {message}")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QColor('#6c757d'))
        item.setFont(QFont('', 10))
        
        table.setItem(0, 0, item)
        table.horizontalHeader().setStretchLastSection(True)
    
    @staticmethod
    def create_info_table(info_dict, title=None):
        """
        Crea una tabla de dos columnas para mostrar información
        Perfecto para: datos de trabajador, cliente, producto, etc.
        
        Args:
            info_dict: Diccionario con {etiqueta: valor}
            title: Título opcional para la tabla
        """
        # Convertir diccionario a lista de listas
        data = [[key, value] for key, value in info_dict.items()]
        
        # Crear tabla
        table = TableManager.create_simple_table(['Campo', 'Valor'], data)
        
        # Personalizar primera columna (etiquetas)
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item:
                item.setForeground(QColor('#495057'))
                item.setFont(QFont('', weight=QFont.Weight.Bold))
        
        return table
    
    @staticmethod
    def format_as_currency(value):
        """Formatea un número como moneda"""
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return str(value)
