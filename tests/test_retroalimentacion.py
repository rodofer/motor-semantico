import json

import pytest

from motor.retroalimentacion import valor_en_paso


@pytest.fixture
def traza():
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        return json.load(archivo)


def test_valor_antes_de_evaluar(traza):
    assert valor_en_paso(traza, 'contador', 6) == 1
    assert valor_en_paso(traza, 'contador', 12) == 3
    assert valor_en_paso(traza, 'suma', 12) == 6


def test_valor_antes_de_existir(traza):
    assert valor_en_paso(traza, 'contador', 1) is None
