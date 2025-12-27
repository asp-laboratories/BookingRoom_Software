import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.RolService import RolService


def test_listar_rol():
    """
    Tests that listar_rol returns a list of roles.
    """
    rol_services = RolService()
    roles = rol_services.listar_rol()
    assert roles is not None
    assert isinstance(roles, list)
    # The test can be improved by checking the content of the list
    # but for now, this is enough to check that the service is working.


def test_obtener_trabajadores_rol():
    """
    Tests that obtener_trabajadores_rol returns a list of workers for a given role.
    """
    rol_services = RolService()
    # I'm using a role that is likely to exist.
    # The test could be improved by first creating a role and then querying for it.
    trabajadores = rol_services.obtener_trabajadores_rol('Predeterminado')
    assert trabajadores is not None
    assert isinstance(trabajadores, list)