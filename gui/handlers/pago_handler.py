from PyQt6.QtWidgets import QMessageBox
from utils.Formato import permitir_ingreso
from gui.recibo import Recibo

class PagoHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.navegacion = self.main_window.navegacion
        self.pagos = self.main_window.pagos
        self.reservacion = self.main_window.reservacion

    def buscar_historial_pagos(self):
        reservacion = self.navegacion.pagosBuscador.text()

        if not reservacion:
            self.navegacion.pagosResultados.setText("Ninguna reservacion seleccionada")
            return 
        
        if not permitir_ingreso(reservacion, 'numint'):
            self.navegacion.pagosResultados.setText("Ingrese un valor numerico valido")
            return 
        else:
            numReser = int(reservacion)

        pagos_reservacion = self.pagos.pagos_reservacion(numReser)

        self.navegacion.pagosResultados.clear()

        if not pagos_reservacion:
            self.navegacion.pagosResultados.setText("No se encontro la reservacion puesta (ingrese otro numero de reservacion)")
            return

        reporte = f" Numero de Reservacion: {pagos_reservacion[0]['numReser']}\n"
        reporte += f" Con fecha para: {pagos_reservacion[0]['fechaEvento']}\n"
        reporte += f" Efectuado por: {pagos_reservacion[0]['nombreFiscal']}\n"
        reporte += "---------------------------------------------------------------------------------------------------------\n"
        total = 0
        for pago in pagos_reservacion:
            reporte += f"\tPago No.{pago['noPago']}\n"
            reporte += f"\tFecha: {pago['tiempo_pago']} 	 Metodo de Pago: {pago['metodo_pago']}\n" 
            reporte += f"\tConcepto de Pago: {pago['concetp_pago']} 	 Monto Pagado: {pago['montoPago']}\n" 
            reporte += f"\tSaldo Pendiente: {pago['saldo']}\n"
            reporte += "------------------------------------------------------------------------------------------------------\n"
            total += float(pago['montoPago'])
        
        reporte += f"Total pagado hasta el momento: ${total}"

        self.navegacion.pagosResultados.setText(reporte)
    
    def registrar_pago_ejecutar(self, numReser: int, montoPago: float, descripcion: str, concepto: str, metodo: str):
        try:
            if self.pagos.hacer_pago(numReser, montoPago, descripcion, concepto, metodo):
                QMessageBox.information(
                    None, 
                    "Pago Registrado", 
                    f"El pago de ${montoPago:.2f} para la Reservación #{numReser} ha sido registrado correctamente."
                )
                
                # Lógica posterior al pago (emisión de recibo y limpieza)
                self.main_window.recibo = Recibo(numReser)
                self.limpiar_pago()
            else:
                QMessageBox.critical(
                    None, 
                    "Error de Transacción", 
                    f"No se pudo completar el pago para la Reservación #{numReser}. Verifique la conexión o el estado de la reserva."
                )
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error de Ejecución", 
                f"Ocurrió un error de base de datos durante el registro del pago: {e}"
            )

    def limpiar_pago(self):
        self.navegacion.reNumReser.clear()
        self.navegacion.reMontoPago.clear()
        self.navegacion.reDescripcion_2.clear()

        checks = [
            self.navegacion.cbTransferencia, self.navegacion.cbTarjeta, self.navegacion.cbNFC, self.navegacion.cbEfectivo, self.navegacion.cbAbono, self.navegacion.cbUnico 
        ]

        for chec in checks:
            chec.setChecked(False)

    def mostrar_descripcion_en_tiempo_real(self):
        reservac = self.navegacion.reNumReser.text().strip()

        if not reservac:
            self.navegacion.reservacionResultados.clear()
            return
        
        if not permitir_ingreso(reservac, 'numint'):
            self.navegacion.reservacionResultados.setText("Escribir solo numero de reservacion")
            return
        else:
            numReser = int(reservac)
        
        decripcon = self.reservacion.reservacion_descripcion(numReser)
        saldo = self.pagos.calcular_saldo(numReser)
        if saldo:
            saldo = round(saldo, 2)
        else:
            saldo = 0

        if saldo < 0.1:
            saldo = 0

        if decripcon:
            self.navegacion.reservacionResultados.setText(f"Reservacion no.{numReser} \n{decripcon} \nSaldo Pendiente: {saldo}")
        else:
            self.navegacion.reservacionResultados.setText(f"Reservacion no.{numReser}\nNo se encontro descripcion")

    def intentar_registrar_pago(self):
        try:
            # --- 1. VALIDACIÓN NUMÉRICA Y MONTO ---
            
            # 1.1. ID de Reservación (int)
            resevacion_txt = self.navegacion.reNumReser.text().strip()
            numReser = int(resevacion_txt) # Lanza ValueError si no es int
    
            # 1.2. Monto de Pago (float)
            mpago_txt = self.navegacion.reMontoPago.text().strip()
            montoPago = float(mpago_txt) # Lanza ValueError si no es float
            
            if montoPago <= 0:
                raise ValueError("Monto Inválido")
    
            # 1.3. Validación de saldo (Lógica de negocio)
            saldo = self.pagos.calcular_saldo(numReser)
            if saldo < montoPago:
                raise ValueError("Monto Excede Saldo")
            
            # Opcional: Agregar el número de reservación a la lista global (si es necesario por diseño) 
            # self.main_window.obtenerNumeroReservacion.append(numReser) # This was in the original code, but it seems to be a global. Let's keep it in the main window.
            
            # --- 2. DETERMINACIÓN DE CONCEPTOS Y MÉTODOS ---
            
            descripcion = self.navegacion.reDescripcion_2.text().strip()
    
            # Concepto (Abono, Pago Único, Liquidación)
            concepto = ""
            if self.navegacion.cbAbono.isChecked():
                concepto = "ABONO"
            elif self.navegacion.cbUnico.isChecked():
                concepto = "PAGOU"
            elif self.pagos.obtener_no_pago(numReser) == 2:
                concepto = "LIQUI"
            
            if not concepto:
                raise ValueError("Concepto Faltante")
                
            # Método de Pago
            metodo = ""
            if self.navegacion.cbEfectivo.isChecked():
                metodo = "EFCTV"
            elif self.navegacion.cbTarjeta.isChecked():
                metodo = "TARJT"
            elif self.navegacion.cbTransferencia.isChecked():
                metodo = "TRANS"
            elif self.navegacion.cbNFC.isChecked():
                metodo = "NFC"
            
            if not metodo:
                raise ValueError("Método Faltante")
    
            # --- 3. CONFIRMACIÓN ---
            if self.main_window.mostrar_confirmacion(
                "Confirmar Registro de Pago", 
                f"¿Deseas registrar un pago de ${montoPago:.2f} (Concepto: {concepto}, Método: {metodo}) para la Reservación #{numReser}?"
            ):
                # 4. Si el usuario confirma, ejecuta la función de negocio
                self.registrar_pago_ejecutar(numReser, montoPago, descripcion, concepto, metodo)
            else:
                QMessageBox.information(
                    None, 
                    "Pago Cancelado", 
                    "La operación de registro de pago ha sido cancelada."
                )
    
        except ValueError as e:
            # Manejo centralizado de errores de validación y conversión ⚠️
            error_type = str(e)
            
            if "invalid literal for int()" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Número de Reservación debe ser un número entero válido."
                )
            elif "invalid literal for float()" in error_type:
                QMessageBox.warning(
                    None, "Datos Inválidos", "El Monto de Pago debe ser un valor numérico válido."
                )
            elif "Monto Inválido" in error_type:
                 QMessageBox.warning(
                    None, "Datos Inválidos", "El Monto de Pago debe ser mayor que cero."
                )
            elif "Monto Excede Saldo" in error_type:
                 QMessageBox.warning(
                    None, "Valor Inválido", "Se está ingresando una cantidad mayor a la deuda restante (Saldo)."
                )
            elif "Concepto Faltante" in error_type:
                 QMessageBox.warning(
                    None, "Faltan Opciones", "Debes seleccionar un concepto de pago (Abono, Único, etc.)."
                )
            elif "Método Faltante" in error_type:
                 QMessageBox.warning(
                    None, "Faltan Opciones", "Debes seleccionar un método de pago."
                )
            else:
                 QMessageBox.critical(
                    None, "Error de Validación", f"Ocurrió un error inesperado al validar: {e}"
                )
        except Exception as e:
            # Manejo de cualquier otro error inesperado (ej. error en pagos.calcular_saldo)
            QMessageBox.critical(
                None, 
                "Error Inesperado", 
                f"Ocurrió un error grave durante el pre-registro: {e}"
            )
