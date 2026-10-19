import json

import pytest

from motor.clasificador import variables_de_control, es_ultima_evaluacion


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_variable_de_control_es_contador(traza):
    assert variables_de_control(traza) == {'contador'}


def test_ultima_evaluacion(traza):
    assert es_ultima_evaluacion(traza, 12) is True
    assert es_ultima_evaluacion(traza, 6) is False


def test_paso_modifica_no_es_ultima_evaluacion(traza):
    assert es_ultima_evaluacion(traza, 4) is False
