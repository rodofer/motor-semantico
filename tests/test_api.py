import json

import pytest
from fastapi.testclient import TestClient

from api.main import app

cliente = TestClient(app)


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_respuesta_correcta(traza):
    cuerpo = {
        'traza': traza,
        'numeroPaso': 4,
        'respuesta': 1,
    }
    respuesta = cliente.post('/validar', json=cuerpo)
    assert respuesta.status_code == 200
    assert respuesta.json() == {
        'numeroPaso': 4,
        'correcto': True,
        'valorEsperado': 1,
        'tipoError': None,
        'mensaje': '¡Bien! Después de contador += 1, contador vale 1.',
    }


def test_booleano_en_paso_modifica_devuelve_422(traza):
    cuerpo = {
        'traza': traza,
        'numeroPaso': 4,
        'respuesta': True,
    }
    respuesta = cliente.post('/validar', json=cuerpo)
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "TipoDeRespuestaInvalido"


def test_respuesta_de_texto_devuelve_422(traza):
    cuerpo = {
        'traza': traza,
        'numeroPaso': 4,
        'respuesta': '1',
    }
    respuesta = cliente.post('/validar', json=cuerpo)
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "SolicitudInvalida"


def test_paso_inexistente_devuelve_422(traza):
    cuerpo = {
        'traza': traza,
        'numeroPaso': 99,
        'respuesta': 1,
    }
    respuesta = cliente.post('/validar', json=cuerpo)
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "PasoInexistente"


def test_version_no_soportada_devuelve_422(traza):
    traza['versionFormato'] = '2.0'
    cuerpo = {
        'traza': traza,
        'numeroPaso': 4,
        'respuesta': 1,
    }
    respuesta = cliente.post('/validar', json=cuerpo)
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "VersionNoSoportada"
