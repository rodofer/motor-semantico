import json

import pytest

from motor.comparador import (
    PasoInexistenteError,
    TipoDeRespuestaInvalidoError,
    buscar_paso,
    comparar,
)


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_buscar_paso_devuelve_paso_solicitado(traza):
    paso = buscar_paso(traza, 4)
    assert paso['numeroPaso'] == 4
    assert paso['instruccion'] == 'contador += 1'


def test_buscar_paso_inexistente(traza):
    with pytest.raises(PasoInexistenteError):
        buscar_paso(traza, 13)


def test_modifica_correcto(traza):
    assert comparar(traza, 4, 1) == (True, 1)


def test_modifica_incorrecto(traza):
    assert comparar(traza, 4, 0) == (False, 1)


def test_evalua_correcto(traza):
    assert comparar(traza, 6, True) == (True, True)


def test_evalua_incorrecto(traza):
    assert comparar(traza, 12, True) == (False, False)


def test_booleano_en_modifica_es_invalido(traza):
    with pytest.raises(TipoDeRespuestaInvalidoError):
        comparar(traza, 4, True)


def test_entero_en_evalua_es_invalido(traza):
    with pytest.raises(TipoDeRespuestaInvalidoError):
        comparar(traza, 6, 1)
