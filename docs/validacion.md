# Contrato del Motor semántico - versión 1.0

## POST /validar

Valida la respuesta del estudiante para un paso de la traza.

### Solicitud

| campo | tipo | descripción |
|---|---|---|
| `traza` | objeto | Traza completa, formato 1.x (ver `docs/traza.md` del Parser) |
| `numeroPaso` | entero ≥ 1 | Paso que el estudiante está respondiendo |
| `respuesta` | entero o booleano | Entero si el paso es `modifica`; booleano si es `evalua` |

### Respuesta (200)

| campo | tipo | descripción |
|---|---|---|
| `numeroPaso` | entero | El mismo de la solicitud |
| `correcto` | booleano | Si la respuesta coincide con la traza experta |
| `valorEsperado` | entero o booleano | Valor correcto; se muestra siempre |
| `tipoError` | texto o `null` | `null` si es correcto; si no, uno de la tabla |
| `mensaje` | texto | Retroalimentación para el estudiante, en español |

### Tipos de error

| `tipoError` | regla (versión 1.0) |
|---|---|
| `VariableDeControlNoActualizada` | Paso `modifica` sobre la variable de control; la respuesta es igual a `valorAnterior` |
| `DesfaseDeConteo` | Paso `evalua` incorrecto, y es la última evaluación de su condición (mismo `@id`), es decir, la que termina el ciclo (off-by-one) |
| `CondicionErronea` | Paso `evalua` incorrecto, en cualquier otra evaluación |
| `ValorIncorrecto` | Cualquier otro error que aún no se clasifica |

**Variable de control:** variable que aparece en `dependeDe` de la Condición
y que es modificada por algún paso dentro del bloque de ese ciclo.

### Errores (422)

Responden `{"detail": {"tipo": "...", "mensaje": "..."}}`.

| `tipo` | situación |
|---|---|
| `PasoInexistente` | `numeroPaso` no existe en la traza |
| `TipoDeRespuestaInvalido` | Entero en un paso `evalua`, o booleano en un paso `modifica` |
| `VersionNoSoportada` | `versionFormato` de la traza no es 1.x |
| `SolicitudInvalida` | Falta un campo o tiene un tipo incorrecto |

## Ejemplos (traza contador_suma)

### Paso 4, respuesta correcta
Solicitud: `numeroPaso: 4, respuesta: 1`
Respuesta: `correcto: true, valorEsperado: 1, tipoError: null`

### Paso 4, variable de control no actualizada
Solicitud: `numeroPaso: 4, respuesta: 0`
Respuesta: `correcto: false, valorEsperado: 1, tipoError: "VariableDeControlNoActualizada"`

### Paso 6, evaluación errónea
Solicitud: `numeroPaso: 6, respuesta: false`
Respuesta: `correcto: false, valorEsperado: true, tipoError: "CondicionErronea"`

### Paso 12, desfase de conteo (off-by-one)
Solicitud: `numeroPaso: 12, respuesta: true`
Respuesta: `correcto: false, valorEsperado: false, tipoError: "DesfaseDeConteo"`

### Paso 5, valor incorrecto no clasificado
Solicitud: `numeroPaso: 5, respuesta: 0`
Respuesta: `correcto: false, valorEsperado: 1, tipoError: "ValorIncorrecto"`
