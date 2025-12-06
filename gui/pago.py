import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.PagoService import PagoServices
from services.ReservacionService import ReservacionService

from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "pago.ui"

pagos = PagoServices()
reservacion = ReservacionService()

class Pago():
    def __init__(self):
        self.pago = uic.loadUi(str(ruta_ui))
        # self.initGUI()
        self.pago.show()
        self.pago.reNumReser.textChanged.connect(self.mostrar_descripcion_en_tiempo_real)
        self.pago.reConfirmar_2.clicked.connect(self.registrar_pago)
        self.pago.reCancelar_2.clicked.connect(self.limpiar_pago)
        
    def registrar_pago(self):
            resevacion = self.pago.reNumReser.text()
            if not permitir_ingreso(resevacion, 'numint'):
                self.pago.reNumReser.selectAll()
                self.pago.reNumReser.setFocus()
                return
            else:
                numReser = int(resevacion)
            
            mpago = self.pago.reMontoPago.text()
            if not permitir_ingreso(mpago, 'numfloat'):
                self.pago.reMontoPago.selectAll()
                self.pago.reMontoPago.setFocus()
                return
            else:
                montoPago = int(mpago)
                saldo = pagos.calcular_saldo(numReser)
                if saldo < montoPago:
                    QMessageBox.warning(self.pago, "Ingresar un valor valido", "Se esta ingresando una cantidad mayor a la deuda.")
                    return
    
            descripcion = self.pago.reDescripcion_2.text()
    
            concepto = ""
            if self.pago.cbAbono.isChecked():
                concepto = "ABONO"
            #elif self.pago.cbLiquidacion.isChecked():
            #    concepto = "LIQUI"
            elif self.pago.cbUnico.isChecked():
                concepto = "PAGOU"
            elif pagos.obtener_no_pago(numReser) == 2:
                concepto = "LIQUI"
                return
            
            metodo = ""
            if self.pago.cbEfectivo.isChecked():
                metodo = "EFCTV"
            elif self.pago.cbTarjeta.isChecked():
                metodo = "TARJT"
            elif self.pago.cbTransferencia.isChecked():
                metodo = "TRANS"
            elif self.pago.cbNFC.isChecked():
                metodo = "NFC"
            else:
                return
            
            if pagos.hacer_pago(numReser, montoPago, descripcion, concepto, metodo):
                self.limpiar_pago()
    
    def limpiar_pago(self):
            self.pago.reNumReser.clear()
            self.pago.reMontoPago.clear()
            self.pago.reDescripcion_2.clear()
    
            checks = [
                self.pago.cbTransferencia, self.pago.cbTarjeta, self.pago.cbNFC, self.pago.cbEfectivo, self.pago.cbAbono, self.pago.cbUnico 
            ]
    
            for chec in checks:
                chec.setChecked(False)
    
    def mostrar_descripcion_en_tiempo_real(self):
            reservac = self.pago.reNumReser.text().strip()
    
            if not reservac:
                self.pago.reservacionResultados.clear()
                return
            
            if not permitir_ingreso(reservac, 'numint'):
                self.pago.reservacionResultados.setText("Escribir solo numero de reservacion")
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
                self.pago.reservacionResultados.setText(f"Reservacion no.{numReser} \n{decripcon} \nSaldo Pendiente: {saldo}")
            else:
                self.pago.reservacionResultados.setText(f"Reservacion no.{numReser}\nNo se encontro descripcion")
    
    
