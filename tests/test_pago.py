import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.PagoService import PagoServices

pago = PagoServices()

def realizar_pago():
    return pago.hacer_pago(44, 1000, 'Pago ola,asa', 'abon', 'tarjeta')

if __name__ == "__main__":
    print(realizar_pago())