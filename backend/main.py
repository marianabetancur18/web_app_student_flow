# External libraries
import uvicorn
from fastapi import FastAPI, APIRouter, Response, File, UploadFile, HTTPException

# Own libraries
from procesamiento.procesamiento_total import procesar_historia

app = FastAPI()

historia = APIRouter(prefix='/historia')


@historia.post('/historia', status_code=200)
async def obtener_historia(
        response: Response,
        archivo_historia: UploadFile = File(...)):
    """Consulta los id y nombres de las cámaras"""
    try:
        texto = archivo_historia.file.read().decode()

        # TODO: completar las funciones de procesar historia
        data = procesar_historia(texto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return data

app.include_router(historia)

if __name__ == '__main__':
    uvicorn.run(app)
