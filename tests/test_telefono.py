import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TelefonoServices import TelefonoServices
telefono = TelefonoServices()
telefono.registrar_telefono(6642081698,None,"SANC870512GRM")
