from horario_simple_corregido import HorarioSimple
from database_simulada import db
from datetime import date
import sys
from PyQt6.QtWidgets import QApplication

def test_manual():
    """Prueba manual de la base de datos"""
    print("🧪 PRUEBA MANUAL DE LA BD")
    print("=" * 50)
    
    # Agregar eventos de prueba directamente
    db.agregar_evento("Reunión de Prueba", date(2024, 1, 15), "19:00", "20:00")
    db.agregar_evento("Clase Python", date(2024, 1, 16), "20:00", "21:00")
    
    print("Eventos en BD:")
    for evento in db.obtener_todos_eventos():
        print(f"  - {evento['nombre']} | {evento['fecha']} | {evento['hora_inicio']}-{evento['hora_fin']}")

if __name__ == "__main__":
    # Ejecutar prueba manual
    test_manual()
    
    # Ejecutar la aplicación
    app = QApplication(sys.argv)
    window = HorarioSimple()
    window.show()
    
    print("\n🎯 INSTRUCCIONES PARA PROBAR:")
    print("1. Configura las fechas para incluir 15/01/2024 y 16/01/2024")
    print("2. Deberías ver los eventos de prueba ya cargados")
    print("3. Agrega nuevos eventos usando el formulario")
    
    sys.exit(app.exec())
