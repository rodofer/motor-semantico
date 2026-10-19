import json

import pytest

from motor.clasificador import variables_de_control


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_variable_de_control_es_contador(traza):
    assert variables_de_control(traza) == {'contador'}
