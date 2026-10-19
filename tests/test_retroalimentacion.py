import json

import pytest

from motor.retroalimentacion import generar_mensaje, describir_estado, valor_en_paso


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


def test_describir_estado_una_variable(traza):
    paso = traza['@graph'][5]
    assert describir_estado(traza, paso) == 'contador = 1'


def test_describir_estado_varias_variables():
    traza = {'@graph': [
        {'numeroPaso': 1, 'modifica': {'variable': 'i', 'valorNuevo': 0}},
        {'numeroPaso': 2, 'modifica': {'variable': 'n', 'valorNuevo': 5}},
        {'numeroPaso': 3, 'evalua': {'dependeDe': ['i', 'n']}},
    ]}
    assert describir_estado(traza, traza['@graph'][2]) == 'i = 0 y n = 5'


def test_mensaje_correcto_modifica(traza):
    assert generar_mensaje(traza, 4, None) == "¡Bien! Después de contador += 1, contador vale 1."


def test_mensaje_variable_de_control(traza):
    mensaje = generar_mensaje(traza, 4, 'VariableDeControlNoActualizada')
    assert 'variable de control' in mensaje
    assert 'vale 1' in mensaje


def test_mensaje_condicion_incluye_estado(traza):
    assert 'contador = 1' in generar_mensaje(traza, 6, 'CondicionErronea')


def test_mensaje_desfase_invita_a_contar(traza):
    mensaje = generar_mensaje(traza, 12, 'DesfaseDeConteo')
    assert 'contador = 3' in mensaje
    assert '¿' in mensaje
