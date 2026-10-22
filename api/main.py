from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StrictInt, StrictBool

from motor.comparador import PasoInexistenteError, TipoDeRespuestaInvalidoError
from motor.pipeline import VersionNoSoportadaError, validar
from motor.validacion import TrazaInvalidaError

app = FastAPI(title="Motor semántico del Depurador Visual Interactivo", version="0.1.1")


class SolicitudValidacion(BaseModel):
    traza: dict
    numeroPaso: int = Field(ge=1)
    respuesta: StrictBool | StrictInt


def error_422(tipo: str, mensaje: str) -> HTTPException:
    return HTTPException(status_code=422, detail={"tipo": tipo, "mensaje": mensaje})


@app.exception_handler(RequestValidationError)
async def solicitud_invalida(request: Request, exc: RequestValidationError) -> JSONResponse:
    mensaje = "; ".join(f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": {"tipo": "SolicitudInvalida", "mensaje": mensaje}},
    )


@app.post('/validar')
def crear_validacion(solicitud: SolicitudValidacion):
    try:
        return validar(solicitud.traza, solicitud.numeroPaso, solicitud.respuesta)
    except TipoDeRespuestaInvalidoError as e:
        raise error_422("TipoDeRespuestaInvalido", str(e)) from e
    except PasoInexistenteError as e:
        raise error_422("PasoInexistente", str(e)) from e
    except VersionNoSoportadaError as e:
        raise error_422("VersionNoSoportada", str(e)) from e
    except TrazaInvalidaError as e:
        raise error_422("TrazaInvalida", str(e)) from e
