from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

# from gui.admin import AdminWindow
from gui.admin_screen import AdministradorScreen
from gui.almacen import Almacenista

# from gui.deftl import DefaultWindow
from gui.navegacion import Navegacion
from gui.recepcionista import Recepcionista
from gui.registro import Registro
from services.LoginService import LoginService

ruta_ui = Path(__file__).parent / "login.ui"


class Login:
    def __init__(self, db_instance):
        # Se recibe y guarda la instancia de la BD.
        self.db = db_instance
        # Se inicializa el servicio de Login con la instancia de la BD.
        self.log_service = LoginService(self.db)
        
        self.login = uic.loadUi(str(ruta_ui))
        self.initGUI()
        self.login.mensaje.setText("")
        self.login.labelLink.linkActivated.connect(self.abrir_registro)
        self.login.show()

    def abrir_registro(self, link):
        if link == "registro":
            self.login.hide()  # Ocultar ventana actual
            self.ventana_registro = Registro(self.db)

    def ingresar(self):
        if len(self.login.leEmail.text()) < 2:
            self.login.mensaje.setText("Ingrese un email valido")
            self.login.leEmail.setFocus()
        elif len(self.login.leNumero.text()) < 2:
            self.login.mensaje.setText("Ingrese un numero de trabajador valido")
            self.login.leNumero.setFocus()
        else:
            self.login.mensaje.setText("")
            # Se usa la instancia de servicio de la clase.
            trabajador = self.log_service.autenticar_trabajador(
                self.login.leEmail.text(), self.login.leNumero.text()
            )
            if trabajador:
                QMessageBox.information(self.login, "Login exitoso", "Credenciales correctas.")
                
                self.login.hide()
                if trabajador.codigoRol == "DEFLT":
                    self.nav = Navegacion(self.db, trabajador)
                elif trabajador.codigoRol == "ADMIN":
                    self.admin = AdministradorScreen(self.db, trabajador)
                elif trabajador.codigoRol == "ALMAC":
                    self.almacen = Almacenista(self.db, trabajador)
                elif trabajador.codigoRol == "RECEP":
                    self.recep = Recepcionista(self.db, trabajador)
            else:
                QMessageBox.warning(self.login, "Error de login", "Credenciales incorrectas.")

    def initGUI(self):
        self.login.btnIniciar.clicked.connect(self.ingresar)
