import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.TipoClienteService import TipoClienteService


def test_listar_clientes_por_tipo():
    """
    Tests that listar_clientes_por_tipo returns a list of clients for a given type.
    """
    tipCliente = TipoClienteService()
    # Using a client type that is likely to exist.
    clientes = tipCliente.listar_clientes_por_tipo("Persona fisica")
    assert clientes is not None
    assert isinstance(clientes, list)