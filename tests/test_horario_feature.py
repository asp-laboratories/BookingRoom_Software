import sys
import os
from datetime import date, timedelta

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDate

# Adjust path to import modules from the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.navegacion import Navegacion
# Assuming HorarioView and HorarioHandler are integrated and managed by Navegacion
# from gui.horario_view import HorarioView 
# from gui.handlers.horario_handler import HorarioHandler

def run_horario_test():
    app = QApplication(sys.argv)

    # Instantiate Navegacion. This will set up HorarioView and HorarioHandler internally.
    main_window_instance = Navegacion()
    
    # The HorarioView is added to Navegacion's stackedWidget.
    # To make it visible directly for testing, we'd need to switch the stackedWidget's index.
    # We need to find the index of the horario_view in the stackedWidget.
    
    # Access the HorarioView instance directly from Navegacion for interaction
    horario_view = main_window_instance.horario_view
    horario_handler = main_window_instance.horario_handler # The handler is also an attribute of Navegacion
    
    # Find the index of horario_view in stackedWidget
    horario_page_index = main_window_instance.navegacion.stackedWidget.indexOf(horario_view)
    if horario_page_index != -1:
        main_window_instance.navegacion.stackedWidget.setCurrentIndex(horario_page_index)
    else:
        print("Error: HorarioView not found in stackedWidget.")
        sys.exit(1)

    # The entire Navegacion window (which now contains HorarioView) needs to be shown
    main_window_instance.navegacion.show()

    # --- Simulate user interaction ---

    # 1. Select a salon (e.g., "Todos los Salones" which is added first)
    # The comboSalon is part of horario_view
    if horario_view.comboSalon.count() > 0:
        # Assuming "Todos los Salones" is the first item (index 0)
        horario_view.comboSalon.setCurrentIndex(0) 
    
    # 2. Set a specific date (e.g., next Monday)
    today = date.today()
    # Calculate next Monday (or today if today is Monday)
    next_monday = today + timedelta(days=(0 - today.weekday() + 7) % 7) 
    horario_view.dateInicio.setDate(QDate(next_monday.year, next_monday.month, next_monday.day))
    
    # 3. Trigger the update
    horario_view.btnActualizar.click()

    print("\n--- Horario Test Iniciado ---")
    print(f"Visualizando horario desde: {next_monday.strftime('%Y-%m-%d')}")
    print(f"Salón seleccionado: {horario_view.comboSalon.currentText()}")
    print("Por favor, inspeccione la ventana abierta para verificar la visualización del horario y los conflictos.")
    print("Asegúrese de que la tabla esté poblada correctamente.")
    print("Cierre la ventana o presione Ctrl+C en la consola para salir.")

    sys.exit(app.exec())

if __name__ == "__main__":
    run_horario_test()
