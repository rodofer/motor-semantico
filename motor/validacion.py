class TrazaInvalidaError(ValueError):
    pass


def revisar_traza(traza: dict) -> None:
    grafo = traza.get('@graph')
    if not isinstance(grafo, list):
        raise TrazaInvalidaError("La traza no tiene el campo @graph (lista)")
