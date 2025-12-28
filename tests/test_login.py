import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.LoginService import LoginService

# Se crea una instancia del servicio que vamos a probar
login_service = LoginService()

def test_login_exitoso(monkeypatch):
    """
    Prueba el escenario de un inicio de sesión exitoso.
    Utiliza monkeypatch para simular una respuesta exitosa del repositorio.
    """
    # 1. Preparación (Arrange)
    email_esperado = "test@example.com"
    num_trabajador_esperado = "12345"
    rol_esperado = "ADMIN"
    respuesta_simulada = [email_esperado, num_trabajador_esperado, rol_esperado]

    # Creamos una función "falsa" que reemplazará al método real
    def mock_iniciar_trabajador(email, numTrabajador):
        return respuesta_simulada

    # Usamos monkeypatch para reemplazar el método real del repositorio con nuestra función falsa
    monkeypatch.setattr(login_service.login_repository, "iniciar_trabajador", mock_iniciar_trabajador)

    # 2. Acción (Act)
    # Llamamos al método del servicio que queremos probar
    resultado = login_service.registrar_trabajadores(email_esperado, num_trabajador_esperado)

    # 3. Aserción (Assert)
    # Verificamos que el resultado es el que esperábamos
    assert resultado is not False
    assert isinstance(resultado, list)
    assert resultado == respuesta_simulada
    assert resultado[0] == email_esperado
    assert resultado[2] == rol_esperado

def test_login_fallido(monkeypatch):
    """
    Prueba el escenario de un inicio de sesión fallido (credenciales incorrectas).
    Utiliza monkeypatch para simular una respuesta fallida del repositorio.
    """
    # 1. Preparación (Arrange)
    email_invalido = "noexiste@example.com"
    num_trabajador_invalido = "00000"
    
    # Creamos una función falsa que simula no encontrar al trabajador
    def mock_iniciar_trabajador_fallido(email, numTrabajador):
        return False

    # Reemplazamos el método real con la función falsa
    monkeypatch.setattr(login_service.login_repository, "iniciar_trabajador", mock_iniciar_trabajador_fallido)

    # 2. Acción (Act)
    resultado = login_service.registrar_trabajadores(email_invalido, num_trabajador_invalido)

    # 3. Aserción (Assert)
    # Verificamos que el resultado sea False, como se esperaba
    assert resultado is False