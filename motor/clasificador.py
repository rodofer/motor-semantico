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
