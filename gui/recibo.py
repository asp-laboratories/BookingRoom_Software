import os
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox 
from services.PagoService import PagoServices
from services.ReservacionService import ReservacionService

from utils.Formato import permitir_ingreso

ruta_ui = Path(__file__).parent / "recibo.ui"

pagos = PagoServices()
reservacion = ReservacionService()



class Recibo():
    def __init__(self, numeroR):
        self.numeroR = numeroR
        self.recibo = uic.loadUi(str(ruta_ui))
        self.recibo.show()
        self.mostrarRecibo()
    #
    # def mostrarRecibo(self):
    #
    #     numeroPago = pagos.obtener_no_pago(self.numeroR)
    #     resultado = pagos.recibo(self.numeroR, numeroPago)
    #     
    #     if not resultado:  # Verifica si la lista está vacía o es None
    #         self.recibo.labelNombreCliente.setText("No hay datos")
    #     else:
    #         # Accede al primer elemento de la lista
    #         self.recibo.labelNombreCliente.setText(f"{resultado[0]['cliente']}")
    #         numeroPago = pagos.obtener_no_pago(self.numeroR)
    #         resultado = pagos.recibo(self.numeroR, numeroPago)
        
    def mostrarRecibo(self):
        numeroPago = pagos.obtener_no_pago(self.numeroR)
        resultado = pagos.recibo(self.numeroR, numeroPago)
        
        if not resultado or len(resultado) == 0:
            self.recibo.labelNombreCliente.setText("No hay datos del cliente")
        else:
            datos = resultado[0]  
            
            self.recibo.labelNombreCliente.setText(f"Nombre del cliente: {datos['cliente']}")
            self.recibo.con.setText(f"Contacto: {datos['contacto']}")
            self.recibo.correoElectronico.setText(f"Correo electronico: {datos['correo']}")
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
