import sys
import os
from datetime import date, timedelta

# Adjust path to import modules from the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.handlers.horario_handler import HorarioHandler
from config.db_settings import BaseDeDatos

def test_horario():
    db_instance = BaseDeDatos()
    db_instance.conectar()
    
    # We need a mock for the main_window, since the handler expects it
    class MockMainWindow:
        def __init__(self, db_instance):
            from services.ReservacionService import ReservacionService
            from services.SalonServices import SalonServices
            # The handler will access services through this mock object
            self.reservacion_service = ReservacionService(db_instance)
            self.salon_service = SalonServices(db_instance)
            
            class MockNavegacion:
                def __init__(self):
                    self.stackedWidget = self
                    self.horario_view = self
                    self.comboSalon = self
                    self.tableWidget = self
                def setCurrentIndex(self, index):
                    pass
                def currentText(self):
                    return "Todos los Salones"
                
                def setColumnCount(self, count):
                    pass
                def setRowCount(self, count):
                    pass
                def setHorizontalHeaderLabels(self, labels):
                    pass
                def setItem(self, row, col, item):
                    pass
                
                def clear(self):
                    pass
            
            self.navegacion = MockNavegacion()
            self.horario_view = self.navegacion
    mock_main_window = MockMainWindow(db_instance)
    horario_handler = HorarioHandler(mock_main_window)
    
    today = date.today()
    next_monday = today + timedelta(days=(0 - today.weekday() + 7) % 7) 
    
    # Directly call the method that updates the schedule
    conflict_data = horario_handler.update_schedule(next_monday, next_monday + timedelta(days=6))
    
    print("\n--- Horario Test Iniciado ---")
    print(f"Visualizando horario desde: {next_monday.strftime('%Y-%m-%d')}")
    print(f"Salón seleccionado: {mock_main_window.comboSalon.currentText()}")
    
    # Assert that the method returns a list (of conflicts)
    assert isinstance(conflict_data, list)
    
    print("Prueba de lógica de horario completada. Se verificó que la actualización devuelve una lista.")
    
    db_instance.desconectar()

if __name__ == "__main__":
    test_horario()
