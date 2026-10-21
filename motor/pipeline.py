from motor.comparador import comparar
from motor.clasificador import clasificar
from motor.retroalimentacion import generar_mensaje
from motor.validacion import revisar_traza

VERSION_SOPORTADA = "1.0"

class VersionNoSoportadaError(ValueError):
    pass


def validar(traza: dict, numero_paso: int, respuesta: int | bool) -> dict:
    version_traza = traza.get('versionFormato')
    if version_traza != VERSION_SOPORTADA:
        raise VersionNoSoportadaError(
            f"La traza tiene la versión {version_traza}, "
            f"el motor soporta la {VERSION_SOPORTADA}"
        )
    revisar_traza(traza)
    tipo_error = None
    correcto, valor_esperado = comparar(traza, numero_paso, respuesta)
    if not correcto:
        tipo_error = clasificar(traza, numero_paso, respuesta)
    return {
        'numeroPaso': numero_paso,
        'correcto': correcto,
        'valorEsperado': valor_esperado,
        'tipoError': tipo_error,
        'mensaje': generar_mensaje(traza, numero_paso, tipo_error),
    }
