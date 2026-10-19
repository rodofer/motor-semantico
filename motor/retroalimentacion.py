from motor.comparador import buscar_paso


def valor_en_paso(traza: dict, variable: str, numero_paso: int) -> int | None:
    """Valor de la variable justo antes de ejecutar el paso indicado."""
    valor = None
    for paso in traza['@graph']:
        if paso['numeroPaso'] >= numero_paso:
            break
        if 'modifica' in paso and paso['modifica']['variable'] == variable:
            valor = paso['modifica']['valorNuevo']
    return valor


def describir_estado(traza: dict, paso: dict) -> str:
    partes = []
    for variable in paso['evalua']['dependeDe']:
        valor = valor_en_paso(traza, variable, paso['numeroPaso'])
        partes.append(f"{variable} = {valor}")
    return " y ".join(partes)


def generar_mensaje(traza: dict, numero_paso: int, tipo_error: str | None) -> str:
    paso = buscar_paso(traza, numero_paso)
    if 'modifica' in paso:
        instruccion = paso['instruccion']
        variable = paso['modifica']['variable']
        valor = paso['modifica']['valorNuevo']
        if tipo_error is None:
            return f"¡Bien! Después de {instruccion}, {variable} vale {valor}."
        if tipo_error == 'VariableDeControlNoActualizada':
            return (f"Ojo: {variable} es la variable de control del ciclo y "
                    f"cambia en cada iteración. Después de {instruccion}, "
                    f"vale {valor}.")
        return (f"Revisa la instrucción: después de {instruccion}, {variable} "
                f"vale {valor}.")

    expresion = paso['evalua']['expresion']
    verdad = "verdadera" if paso['resultado'] else "falsa"
    if tipo_error is None:
        consecuencia = "así que el ciclo sigue" if paso['resultado'] else "así que el ciclo termina"
        return f"¡Bien! {expresion} es {verdad}, {consecuencia}."
    estado = describir_estado(traza, paso)
    if tipo_error == 'DesfaseDeConteo':
        return (f"Cuenta bien las vueltas: con {estado}, {expresion} es "
                f"{verdad} y el ciclo termina. ¿Cuántas veces se ejecutó "
                "el cuerpo?")
    return f"Revisa la condición: con {estado}, {expresion} es {verdad}."
