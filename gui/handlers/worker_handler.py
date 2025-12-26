from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QSize
from models.ReserEquipa import ReserEquipamiento

class WorkerHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.trabajador = self.main_window.trabajador
        self.rol_service = self.main_window.TrabajadorRol
        self.telefono_service = self.main_window.telefono
        self.reservacion_service = self.main_window.reservacion

    def buscar(self):
        rfc = self.navegacion.atRFC.text()
        resultado = self.trabajador.buscar_trabajador(rfc)
        resul_telefono = self.telefono_service.listar_telefonos_info(rfc)
        
        if not resultado:
            self.navegacion.atOutput.setText("No se encontraron resultados")
            return
        
        mensaje = "INFORMACION DEL TRABAJADOR\n"
        mensaje += f"\nNombre: {resultado['nombre']} {resultado['priApe']} {resultado['segApe']}\n"
        mensaje += f"\nRFC: {resultado['RFC']}\n"
        mensaje += f"\nNumero de trabajador: {resultado['numTraba']}\n"
        mensaje += f"\nRol: {resultado['rol']}\n"
        mensaje += f"\nCorreo: {resultado['email']}\n"
        mensaje += "\nTelefonos:\n"
        
        contador = 0
        for cel in resul_telefono:
            contador += 1
            if not cel['telefono'] == "":
                mensaje += f"{contador}: {cel['telefono']}\n"
                
        self.navegacion.atOutput.setText(mensaje)

    def buscar_sus_reservaciones(self):
        rfc = self.navegacion.atRFC_2.text()
        resultado = self.reservacion_service.reservaciones_trabajador(rfc)
        
        if not resultado:
            self.navegacion.atOutput_2.setText("No se encontraron resultados")
            return
        
        mensaje = ""
        for reser in resultado:
            mensaje += f"Numero de reservacion: {reser['numReser']}\n"
            mensaje += f"Fecha de la reservacion: {reser['fechaReser']}\n"
            mensaje += f"Fecha del evento: {reser['fecha']}\n"
            mensaje += "--------------------------------------------------------\n"
            
        self.navegacion.atOutput_2.setText(mensaje)

    def establecer_rol(self):
        rol = self.navegacion.atRol.text()
        rfc = self.navegacion.atRFC_3.text()
        resultado = self.trabajador.establecer_rol(rol, rfc)
        
        if not resultado:
            self.navegacion.atOutput_3.setText("No se encontraron resultados")
            return
        
        self.navegacion.atOutput_3.setText("Rol establecido con éxito")
    
    def intentar_establecer_rol(self):
        if self.main_window.mostrar_confirmacion("Confirmar rol", "¿Desea confirmar rol?"):
            self.establecer_rol()
        else:
            self.navegacion.atOutput_3.setText("Rol no establecido")

    def llenar_combox_roles(self):
        self.navegacion.rolBuscadorTrabajadores.clear()
        self.navegacion.rolBuscadorTrabajadores.addItem("Selecciona un rol", None)
        roles = self.rol_service.listar_rol()
        for rol in roles:
            self.navegacion.rolBuscadorTrabajadores.addItem(rol['descripcion'], rol['descripcion'])

    def llenar_lista_trabajadores(self):
        self.navegacion.rolTrabajadores.clear()
        self.navegacion.rolDetalleTrabajador.clear()
        rol_obtenido = self.navegacion.rolBuscadorTrabajadores.currentText()
        if not rol_obtenido:
            QMessageBox.warning(self.navegacion, "Rol no seleccionado", "Favor de seleccionar un rol para buscar")
            return
        trabajadores = self.rol_service.obtener_trabajadores_rol(rol_obtenido)
        for traba in trabajadores:
            item = QListWidgetItem(self.navegacion.rolTrabajadores)
            item.setSizeHint(QSize(0, 60))
            item.setData(Qt.ItemDataRole.UserRole, traba)
            tarjeta = self.tarjeta_trabajador(traba)
            self.navegacion.rolTrabajadores.setItemWidget(item, tarjeta)

    def detalles_trabajador(self, item):
        self.navegacion.rolDetalleTrabajador.clear()
        traba = item.data(Qt.ItemDataRole.UserRole)
        infoTrabajador = f"\n---{traba['nombre']}---\n"
        infoTrabajador += f"Numero de trabajador: {traba['numTraba']}\n"
        infoTrabajador += f"RFC: {traba['RFC']}\n"
        infoTrabajador += "\n---CONTACTO---\n"
        infoTrabajador += f"Correo Electronico: {traba['email']}\n"
        infoTrabajador += "--Telefonos:\n"
        contador = 0
        for telef in traba['telefonos']:
            contador += 1
            infoTrabajador += f"{contador}. {telef}\n"
        self.navegacion.rolDetalleTrabajador.setText(infoTrabajador)
        
    def tarjeta_trabajador(self, trabajador): 
        widget = QWidget()
        layoutTar = QVBoxLayout()
        widget.setLayout(layoutTar)

        widget.setStyleSheet("""
        QWidget {
            background-color: transparent;
        }
        QLabel {
            background-color: transparent;
        }
        """)

        label_nombre = QLabel(trabajador['nombre'])
        label_nombre.setStyleSheet("""
                color: rgb(0, 0, 0);
                border-radius: 5px;
                border-bottom: 3px solid rgba(155, 88, 43, 1.0);
                border-right: 3px solid  rgba(155, 88, 43, 1.0);
                """,)
        
        label_id = QLabel(f"ID: {trabajador['numTraba']}")
        label_id.setStyleSheet("""
                color: rgb(0, 0, 0);
                border-radius: 5px;
                border-bottom: 3px solid rgba(155, 88, 43, 1.0);
                border-right: 3px solid  rgba(155, 88, 43, 1.0);
                """,)
        
        layoutTar.addWidget(label_nombre)
        layoutTar.addWidget(label_id)

        return widget
