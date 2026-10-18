import json

import pytest

from motor.comparador import (
    PasoInexistenteError,
    buscar_paso,
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
