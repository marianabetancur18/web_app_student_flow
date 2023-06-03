# External libraries
import uvicorn
from fastapi import FastAPI, APIRouter, Response, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Own libraries
from procesamiento.procesamiento_total import procesar_historia

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

historia = APIRouter()


@historia.post('/history', status_code=200)
async def obtener_historia(
        response: Response,
        file: UploadFile):
    try:
        texto = file.file.read().decode()
        # TODO: completar las funciones de procesar historia
        data = procesar_historia(texto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return data

app.include_router(historia)

if __name__ == '__main__':
    uvicorn.run(app)
