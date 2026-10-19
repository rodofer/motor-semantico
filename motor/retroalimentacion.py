def valor_en_paso(traza: dict, variable: str, numero_paso: int) -> int | None:
    valor = None
    for paso in traza['@graph']:
        if paso['numeroPaso'] >= numero_paso:
            break
        if 'modifica' in paso and paso['modifica']['variable'] == variable:
            valor = paso['modifica']['valorNuevo']
    return valor
