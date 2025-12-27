from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from gui.recibo import Recibo
from services.PagoService import PagoServices
from services.ReservacionService import ReservacionService

from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "pago.ui"

pagos = PagoServices()
reservacion = ReservacionService()

numeroReservacion = []


class Pago:
    def __init__(self):
        self.pago = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.pago.show()
        self.pago.reNumReser.textChanged.connect(
            self.mostrar_descripcion_en_tiempo_real
        )
        self.pago.reConfirmar_2.clicked.connect(self.intentar_registrar_pago)
        self.pago.reCancelar_2.clicked.connect(self.limpiar_pago)

    def registrar_pago_ejecutar(
        self,
        numReser: int,
        montoPago: float,
        descripcion: str,
        concepto: str,
        metodo: str,
    ):
        try:
            if pagos.hacer_pago(numReser, montoPago, descripcion, concepto, metodo):
                QMessageBox.information(
                    None,
                    "Pago Registrado",
                    f"El pago de ${montoPago:.2f} para la Reservación #{numReser} ha sido registrado correctamente.",
                )

                # Lógica posterior al pago (emisión de recibo y limpieza)
                self.recibo = Recibo(numReser)
                self.limpiar_pago()
            else:
                QMessageBox.critical(
                    None,
                    "Error de Transacción",
                    f"No se pudo completar el pago para la Reservación #{numReser}. Verifique la conexión o el estado de la reserva.",
                )
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error de Ejecución",
                f"Ocurrió un error de base de datos durante el registro del pago: {e}",
            )

    def limpiar_pago(self):
        self.pago.reNumReser.clear()
        self.pago.reMontoPago.clear()
        self.pago.reDescripcion_2.clear()

        checks = [
            self.pago.cbTransferencia,
            self.pago.cbTarjeta,
            self.pago.cbNFC,
            self.pago.cbEfectivo,
            self.pago.cbAbono,
            self.pago.cbUnico,
        ]

        for chec in checks:
            chec.setChecked(False)

    def mostrar_descripcion_en_tiempo_real(self):
        reservac = self.pago.reNumReser.text().strip()

        if not reservac:
            self.pago.reservacionResultados.clear()
            return

        if not permitir_ingreso(reservac, "numint"):
            self.pago.reservacionResultados.setText(
                "Escribir solo numero de reservacion"
            )
            return
        else:
            numReser = int(reservac)

        decripcon = reservacion.reservacion_descripcion(numReser)
        saldo = pagos.calcular_saldo(numReser)
        if saldo:
            saldo = round(saldo, 2)
        else:
            saldo = 0

        if saldo < 0.1:
            saldo = 0

        if decripcon:
            self.pago.reservacionResultados.setText(
                f"Reservacion no.{numReser} \n{decripcon} \nSaldo Pendiente: {saldo}"
            )
        else:
            self.pago.reservacionResultados.setText(
                f"Reservacion no.{numReser}\nNo se encontro descripcion"
            )

    def intentar_registrar_pago(self):
        try:
            resevacion_txt = self.pago.reNumReser.text().strip()
            numReser = int(resevacion_txt)  # Lanza ValueError si no es int

            mpago_txt = self.pago.reMontoPago.text().strip()
            montoPago = float(mpago_txt)  # Lanza ValueError si no es float

            if montoPago <= 0:
                raise ValueError("Monto Inválido")

            saldo = pagos.calcular_saldo(numReser)
            if saldo < montoPago:
                raise ValueError("Monto Excede Saldo")

            numeroReservacion.append(numReser)

            descripcion = self.pago.reDescripcion_2.text().strip()

            concepto = ""
            if self.pago.cbAbono.isChecked():
                concepto = "ABONO"
            elif self.pago.cbUnico.isChecked():
                concepto = "PAGOU"
            elif pagos.obtener_no_pago(numReser) == 2:
                concepto = "LIQUI"

            if not concepto:
                raise ValueError("Concepto Faltante")

            metodo = ""
            if self.pago.cbEfectivo.isChecked():
                metodo = "EFCTV"
            elif self.pago.cbTarjeta.isChecked():
                metodo = "TARJT"
            elif self.pago.cbTransferencia.isChecked():
                metodo = "TRANS"
            elif self.pago.cbNFC.isChecked():
                metodo = "NFC"

            if not metodo:
                raise ValueError("Método Faltante")

            if self.mostrar_confirmacion(
                "Confirmar Registro de Pago",
                f"¿Deseas registrar un pago de ${montoPago:.2f} (Concepto: {concepto}, Método: {metodo}) para la Reservación #{numReser}?",
            ):
                self.registrar_pago_ejecutar(
                    numReser, montoPago, descripcion, concepto, metodo
                )
            else:
                QMessageBox.information(
                    None,
                    "Pago Cancelado",
                    "La operación de registro de pago ha sido cancelada.",
                )

        except ValueError as e:
            error_type = str(e)

            if "invalid literal for int()" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Número de Reservación debe ser un número entero válido.",
                )
            elif "invalid literal for float()" in error_type:
                QMessageBox.warning(
                    None,
                    "Datos Inválidos",
                    "El Monto de Pago debe ser un valor numérico válido.",
                )
            elif "Monto Inválido" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Monto de Pago debe ser mayor que cero."
                )
            elif "Monto Excede Saldo" in error_type:
                QMessageBox.warning(
                    None,
                    "Valor Inválido",
                    "Se está ingresando una cantidad mayor a la deuda restante (Saldo).",
                )
            elif "Concepto Faltante" in error_type:
                QMessageBox.warning(
                    None,
                    "Faltan Opciones",
                    "Debes seleccionar un concepto de pago (Abono, Único, etc.).",
                )
            elif "Método Faltante" in error_type:
                QMessageBox.warning(
                    None, "Faltan Opciones", "Debes seleccionar un método de pago."
                )
            else:
                QMessageBox.critical(
                    None,
                    "Error de Validación",
                    f"Ocurrió un error inesperado al validar: {e}",
                )
        except Exception as e:
            # Manejo de cualquier otro error inesperado (ej. error en pagos.calcular_saldo)
            QMessageBox.critical(
                None,
                "Error Inesperado",
                f"Ocurrió un error grave durante el pre-registro: {e}",
            )

    def mostrar_confirmacion(self, titulo: str, mensaje: str) -> bool:
        reply = QMessageBox.question(
            None,
            titulo,
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        return reply == QMessageBox.StandardButton.Yes
