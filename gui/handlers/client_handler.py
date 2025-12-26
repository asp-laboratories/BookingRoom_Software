from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QSize
from gui.registro_cliente import RegistroCliente
from utils.Formato import permitir_ingreso

class ClientHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.cliente = self.main_window.cliente
        self.telefono = self.main_window.telefono
        self.TipoCliente = self.main_window.TipoCliente

    def abrir_registro_cliente(self):
        self.main_window.cliente_window = RegistroCliente()

    def buscar_cliente(self):
        rfc = self.navegacion.reRfc.text()
        if not permitir_ingreso(rfc, 'rfc'):
            QMessageBox.warning(self.navegacion, "Error al ingresar datos", "Valores no validos como RFC, ingrese valores validos")
            return

        resultado = self.cliente.listar_cliente_busqueda(rfc)
        resul_telefono = self.telefono.listar_telefonos_info(rfc)
        
        if resultado is None:
            self.navegacion.registrarCliente.setVisible(True)
            QMessageBox.information(self.navegacion, "Cliente no encontrado",  f"No se encontró ningún cliente con el RFC: {self.navegacion.reRfc.text()}")
            self.navegacion.cliente_info.setText(f"No se encontro ningun cliente con el RFC: {self.navegacion.reRfc.text()}, debes registrarlo.")
        else:
            mensaje = "INFORMACION DEL CLIENTE\n"
            mensaje += f"\nNombre completo del contacto: {resultado['contNombre']} {resultado['contPriApellido']}  {resultado['contSegApellido']}\n"
            mensaje += f"\nNombre fiscal: {resultado['nombreFiscal']}\n"
            mensaje += f"\nCorreo electronico: {resultado['email']}\n"
            mensaje += "\nTelefonos:\n"
            self.main_window.clienteNombre = f"{resultado['nombreFiscal']}"
            contador = 0
            for cel in resul_telefono:
                contador += 1
                if not cel['telefono'] == "":
                    mensaje += f"{contador}: {cel['telefono']}\n"
            mensaje += f"\nColonia: {resultado['dirColonia']}\n"
            mensaje += f"\nCalle: {resultado['dirCalle']}\n"
            mensaje += f"\nNumero: {resultado['dirNumero']}\n"
            self.navegacion.cliente_info.setText(mensaje)

    def mostrar_clientes_por_tipo(self):
        self.navegacion.clClientesTipo.clear()
        self.navegacion.clDetalleCliente.clear()
        tipo_cliente = ''
        if self.navegacion.clPersonaFisica.isChecked():
            tipo_cliente = 'Persona fisica'
        elif self.navegacion.clPersonaMoral.isChecked():
            tipo_cliente = 'Persona moral'
        clientes = self.TipoCliente.listar_clientes_por_tipo(tipo_cliente)
        for cliente in clientes:
            item = QListWidgetItem(self.navegacion.clClientesTipo)
            item.setSizeHint(QSize(0, 60))
            item.setData(Qt.ItemDataRole.UserRole, cliente)
            tarjeta = self.tarjeta_cliente(cliente)
            self.navegacion.clClientesTipo.setItemWidget(item, tarjeta)

    def tarjeta_cliente(self, cliente): 
        widget = QWidget()
        layoutTar = QVBoxLayout()
        widget.setLayout(layoutTar)
        widget.setStyleSheet("background-color: transparent;")
        label_nombre = QLabel(cliente['contacto'])
        label_nombre.setStyleSheet("color: rgb(0, 0, 0); border-radius: 5px; border-bottom: 3px solid rgba(155, 88, 43, 1.0); border-right: 3px solid  rgba(155, 88, 43, 1.0);")
        label_id = QLabel(f"ID: {cliente['RFC']}")
        label_id.setStyleSheet("color: rgb(0, 0, 0); border-radius: 5px; border-bottom: 3px solid rgba(155, 88, 43, 1.0); border-right: 3px solid  rgba(155, 88, 43, 1.0);")
        layoutTar.addWidget(label_nombre)
        layoutTar.addWidget(label_id)
        return widget

    def detalle_cliente(self, item):
        self.navegacion.clDetalleCliente.clear()
        clien = item.data(Qt.ItemDataRole.UserRole)
        infoTrabajador = f"\n---{clien['nombreFiscal']}---\n"
        infoTrabajador += f"Contacto: {clien['contacto']}\n"
        infoTrabajador += f"RFC: {clien['RFC']}\n"
        infoTrabajador += "\n---CONTACTO---\n"
        infoTrabajador += f"Direccion: {clien['direccion']}\n"
        infoTrabajador += f"Correo Electronico: {clien['email']}\n"
        infoTrabajador += "--Telefonos:\n"
        contador = 0
        for telef in clien['telefonos']:
            contador += 1
            infoTrabajador += f"{contador}. {telef}\n"
        self.navegacion.clDetalleCliente.setText(infoTrabajador)
