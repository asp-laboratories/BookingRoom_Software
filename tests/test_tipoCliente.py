import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.TipoClienteService import TipoClienteService

tipCliente = TipoClienteService()

print(tipCliente.listar_clientes_por_tipo('Persona fisica'))