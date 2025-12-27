from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from services.PagoService import PagoServices
from services.ReservacionService import ReservacionService


ruta_ui = Path(__file__).parent / "recibo.ui"

pagos = PagoServices()
reservacion = ReservacionService()


class Recibo:
    def __init__(self, numeroR):
        self.numeroR = numeroR
        self.recibo = uic.loadUi(str(ruta_ui))
        self.recibo.show()
        self.mostrarRecibo()

        self.recibo.guardarImagen.clicked.connect(self.guardar_imagen)

    def mostrarRecibo(self):
        numeroPago = pagos.obtener_no_pago(self.numeroR)
        resultado = pagos.recibo(self.numeroR, numeroPago)

        if not resultado or len(resultado) == 0:
            self.recibo.labelNombreCliente.setText("No hay datos del cliente")
        else:
            datos = resultado[0]

            servicios_set = set()
            equipamientos_set = set()
            telefonos_set = set()

            for fila in resultado:
                servicios_set.add(fila["servicio"])
                equipamientos_set.add(fila["equipamiento"])
                telefonos_set.add(fila["telefonos"])

            servicios = ", ".join(sorted(servicios_set))
            equipamientos = ", ".join(sorted(equipamientos_set))
            telefonos = ", ".join(sorted(telefonos_set))

            self.recibo.labelNombreCliente.setText(
                f"Nombre del cliente: {datos['cliente']}"
            )
            self.recibo.con.setText(f"Nombre del contacto: {datos['contacto']}")
            self.recibo.corrreoElectronico.setText(
                f"Correo electronico: {datos['correo']}"
            )
            self.recibo.Ubicacion.setText(f"Dirrecion: {datos['dirrecion']}")
            self.recibo.labelTrabajador.setText(f"Atendido por: {datos['trabajador']}")
            self.recibo.labelSub.setText(f"Subtotal: {datos['subtotal']}")
            self.recibo.labelTotal.setText(f"Total: {datos['total']}")
            self.recibo.labelIVA.setText(f"IVA: {datos['IVA']}")
            self.recibo.labelMontaje.setText(f"Montaje: {datos['montaje']}")
            self.recibo.labelSalon.setText(f"Salon: {datos['salon']}")
            self.recibo.labelMonto.setText(f"Monto: {datos['monto']}")
            self.recibo.labelSaldo.setText(f"Saldo: {datos['saldo']}")
            self.recibo.hora.setText(f"Hora: {datos['hora']}")
            self.recibo.labelFecha.setText(f"Fecha: {datos['fecha']}")
            self.recibo.num.setText(f"Pago Nº{numeroPago}")
            self.recibo.labelServicio.setText(f"Servicios: {servicios}")
            self.recibo.labelEquipamiento.setText(f"Equipamientos: {equipamientos}")
            self.recibo.telefonos.setText(f"Telefonos: {telefonos}")

    def guardar_imagen(self):
        """Guarda el frame 'mi_frame' como imagen PNG en la ruta elegida"""
        try:
            widget = self.recibo.reciboFrame

            pixmap = QPixmap(widget.size())

            pixmap.fill(Qt.GlobalColor.white)

            painter = QPainter(pixmap)
            widget.render(painter)
            painter.end()

            ruta_archivo, _ = QFileDialog.getSaveFileName(
                None,  # Ventana padre
                "Guardar imagen como...",  # Título del diálogo
                "recibo.png",  # Nombre sugerido
                "Imagen PNG (*.png);;"  # Filtros
                "Imagen JPEG (*.jpg *.jpeg);;"
                "Todos los archivos (*)",
            )

            if ruta_archivo:
                pixmap.save(ruta_archivo)

                QMessageBox.information(
                    None, "¡Éxito!", f"Imagen guardada en:\n{ruta_archivo}"
                )

                print(f"✓ Imagen guardada: {ruta_archivo}")
            else:
                print("✗ Operación cancelada por el usuario")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo guardar:\n{str(e)}")
