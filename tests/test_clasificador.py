import json

import pytest

from motor.clasificador import clasificar, es_ultima_evaluacion, variables_de_control


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


def test_variable_de_control_no_actualizada(traza):
    assert clasificar(traza, 4, 0) == 'VariableDeControlNoActualizada'


def test_variable_de_control_con_otro_valor(traza):
    assert clasificar(traza, 4, 5) == 'ValorIncorrecto'


def test_acumulador_no_es_variable_de_control(traza):
    assert clasificar(traza, 5, 0) == 'ValorIncorrecto'


def test_condicion_erronea(traza):
    assert clasificar(traza, 6, False) == 'CondicionErronea'


def test_desfase_de_conteo(traza):
    assert clasificar(traza, 12, True) == 'DesfaseDeConteo'
