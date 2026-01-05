import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from gui.login import Login
from config.db_settings import BaseDeDatos


class BookingRoom:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        db_instance = None
        try:
            # 1. Se crea UNA instancia de la base de datos.
            db_instance = BaseDeDatos()
            
            # 2. Se conecta UNA SOLA VEZ al inicio.
            if not db_instance.conectar():
                QMessageBox.critical(None, "Error de Base de Datos", "No se pudo conectar a la base de datos. La aplicación se cerrará.")
                return

            # 3. Se pasa la instancia a la ventana de Login.
            self.login = Login(db_instance)
            
            # La aplicación se ejecuta.
            sys.exit(self.app.exec())

        finally:
            # 4. Al salir de la app, se desconecta UNA SOLA VEZ.
            if db_instance and db_instance.connection:
                db_instance.desconectar()
                print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    BookingRoom()
