# External libraries
import uvicorn
from fastapi import FastAPI, APIRouter, Response, File, UploadFile, HTTPException
from tempfile import TemporaryFile

# Own libraries
from procesamiento.procesamiento_total import procesar_historia

app = FastAPI()

historia = APIRouter(prefix='/historia')


@historia.get('/historia', status_code=200)
async def obtener_historia(
        response: Response,
        archivo_historia: UploadFile = File(...)):
    """Consulta los id y nombres de las cámaras"""
    try:
        async with archivo_historia.file as archivo_temporal:
            with TemporaryFile(mode="w+") as archivo_en_memoria:
                contenido = archivo_temporal.read()
                archivo_en_memoria.write(contenido)
                archivo_en_memoria.seek(0)
                texto = archivo_en_memoria.read()

        data = procesar_historia(texto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return data, 200

app.include_router(historia)

if __name__ == '__main__':
    uvicorn.run(app)
