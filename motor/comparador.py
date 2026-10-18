class PasoInexistenteError(ValueError):
    pass


class TipoDeRespuestaInvalidoError(ValueError):
    pass


def buscar_paso(traza: dict, numero_paso: int) -> dict:
    for paso in traza['@graph']:
        if paso['numeroPaso'] == numero_paso:
            return paso
    raise PasoInexistenteError(f"La traza no tiene el paso {numero_paso}")


def comparar(traza: dict, numero_paso: int, respuesta: int | bool) -> tuple[bool, int | bool]:
    paso = buscar_paso(traza, numero_paso)
    if 'modifica' in paso:
        tipo_esperado = int
        valor_esperado = paso['modifica']['valorNuevo']
        descripcion = "un número entero"
    else:
        tipo_esperado = bool
        valor_esperado = paso['resultado']
        descripcion = "verdadero o falso"
    if type(respuesta) is not tipo_esperado:
        raise TipoDeRespuestaInvalidoError(f"El paso {numero_paso} espera {descripcion}")
    return respuesta == valor_esperado, valor_esperado
