from motor.comparador import buscar_paso


def variables_de_control(traza: dict) -> set[str]:
    resultado = set()
    for paso in traza['@graph']:
        if 'evalua' in paso:
            dependencias = set(paso['evalua']['dependeDe'])
            modificadas = set()
            for otro in traza['@graph']:
                if 'modifica' in otro and otro['bloque'] == paso['bloque']:
                    modificadas.add(otro['modifica']['variable'])
            resultado |= dependencias & modificadas
    return resultado


def es_ultima_evaluacion(traza: dict, numero_paso: int) -> bool:
    paso = buscar_paso(traza, numero_paso)
    if 'evalua' not in paso:
        return False
    id_condicion = paso['evalua']['@id']
    evaluaciones = []
    for otro in traza['@graph']:
        if 'evalua' in otro and otro['evalua']['@id'] == id_condicion:
            evaluaciones.append(otro['numeroPaso'])
    return numero_paso == max(evaluaciones)
