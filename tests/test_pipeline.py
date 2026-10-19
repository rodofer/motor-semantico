import json

import pytest

from motor.comparador import PasoInexistenteError, TipoDeRespuestaInvalidoError
from motor.pipeline import VersionNoSoportadaError, validar


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_respuesta_correcta(traza):
    assert validar(traza, 4, 1) == {
        'numeroPaso': 4,
        'correcto': True,
        'valorEsperado': 1,
        'tipoError': None,
        'mensaje': '¡Bien! Después de contador += 1, contador vale 1.',
    }


def test_respuesta_incorrecta_clasifica(traza):
    resultado = validar(traza, 4, 0)
    assert resultado['correcto'] is False
    assert resultado['valorEsperado'] == 1
    assert resultado['tipoError'] == 'VariableDeControlNoActualizada'


def test_paso_inexistente(traza):
    with pytest.raises(PasoInexistenteError):
        validar(traza, 99, 1)


def test_tipo_invalido(traza):
    with pytest.raises(TipoDeRespuestaInvalidoError):
        validar(traza, 4, True)


def test_version_no_soportada(traza):
    traza['versionFormato'] = '2.0'
    with pytest.raises(VersionNoSoportadaError):
        validar(traza, 4, 1)


def test_traza_sin_version(traza):
    del traza['versionFormato']
    with pytest.raises(VersionNoSoportadaError):
        validar(traza, 4, 1)
