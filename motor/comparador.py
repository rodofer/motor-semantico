class PasoInexistenteError(ValueError):
    pass


def buscar_paso(traza, numero_paso):
    for paso in traza['@graph']:
        if paso['numeroPaso'] == numero_paso:
            return paso
    raise PasoInexistenteError(f"La traza no tiene el paso {numero_paso}")
