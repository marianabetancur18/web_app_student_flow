# External libraries
import uvicorn
import re
import pandas as pd
from io import StringIO

from fastapi import FastAPI, APIRouter, Response

app = FastAPI()

historia = APIRouter(prefix='/historia')

historia_academica = """Logo UniversidadPORTAL DE SERVICIOS ACADÉMICOS
dadazam
	Datos personales

	Información académica

Mi historia académica
Mis Calificaciones
Mi horario
Mis planes
	Proceso de inscripción

	Buscador de cursos

	Catálogo prog. curriculares

	Información Financiera

	Trámites y solicitudes

	Evaluación docente

Historia Académica


Plan de estudios	
3534 INGENIERÍA DE SISTEMAS E INFORMÁTICA
INGENIERÍA DE SISTEMAS E INFORMÁTICA
Facultad: FACULTAD DE MINAS
Hist. Acad.: 34ESTADO ABIERTO
Resumen
4,6 (Acumulado)
Pregrado - P.A.P.A
2022-2S
4,6 (Acumulado)
Pregrado - Promedio académico
2022-2S
Asignaturas
ASIGNATURAS
CRÉDITOS
TIPO
PERIODO
CALIFICACIÓN
Sistema de Recuperación de Información de Web (3007860)	3	DISCIPLINAR OPTATIVA	2022-2S Ordinaria	4.6
APROBADA
TÉCNICAS EN APRENDIZAJE ESTADÍSTICO (3007854)	3	DISCIPLINAR OPTATIVA	2022-2S Ordinaria	4.6
APROBADA
REDES Y TELECOMUNICACIONES I (3007865)	3	DISCIPLINAR OBLIGATORIA	2022-2S Ordinaria	4.2
APROBADA
Visión Artificial (3009550)	3	LIBRE ELECCIÓN	2022-2S Ordinaria	5.0
APROBADA
ESTRUCTURA DE DATOS (3007741)	3	DISCIPLINAR OBLIGATORIA	2022-1S Ordinaria	4.2
APROBADA
Introducción a la inteligencia artificial (3010476)	3	DISCIPLINAR OBLIGATORIA	2022-1S Ordinaria	4.1
APROBADA
SISTEMAS OPERATIVOS (3007867)	3	DISCIPLINAR OBLIGATORIA	2022-1S Ordinaria	4.4
APROBADA
CÁTEDRA EN INGENIERÍA ELÉCTRICA (3007786)	3	LIBRE ELECCIÓN	2022-1S Ordinaria	4.2
APROBADA
ESTADÍSTICA II (3006915)	4	FUND. OPTATIVA	2021-2S Ordinaria	4.6
APROBADA
ARQUITECTURA DE COMPUTADORES (3007863)	3	DISCIPLINAR OBLIGATORIA	2021-2S Ordinaria	5.0
APROBADA
BASE DE DATOS I (3007847)	3	DISCIPLINAR OBLIGATORIA	2021-2S Ordinaria	4.6
APROBADA
Fundamentos de analítica (3011020)	3	DISCIPLINAR OBLIGATORIA	2021-2S Ordinaria	5.0
APROBADA
Introducción al análisis de decisiones (3010415)	3	DISCIPLINAR OBLIGATORIA	2021-2S Ordinaria	4.6
APROBADA
PROGRAMACIÓN ORIENTADA A OBJETOS (3007744)	3	DISCIPLINAR OBLIGATORIA	2021-2S Ordinaria	4.9
APROBADA
Fundamentos de proyectos en ingeniería (3010408)	3	DISCIPLINAR OBLIGATORIA	2021-1S Ordinaria	4.3
APROBADA
INGENIERÍA DE SOFTWARE (3007853)	3	DISCIPLINAR OBLIGATORIA	2021-1S Ordinaria	4.7
APROBADA
INVESTIGACIÓN DE OPERACIONES I (3007324)	3	DISCIPLINAR OBLIGATORIA	2021-1S Ordinaria	4.7
APROBADA
Teoría de lenguajes de programación (3010426)	3	DISCIPLINAR OBLIGATORIA	2021-1S Ordinaria	4.5
APROBADA
Fundamentos de matemáticas (3010334)	4	LIBRE ELECCIÓN	2021-1S Ordinaria	4.9
APROBADA
Práctica Académica Especial 2 (3007586)	4	LIBRE ELECCIÓN	2021-1S Ordinaria	5.0
APROBADA
Estadística I (3010651)	3	FUND. OBLIGATORIA	2020-2S Ordinaria	4.3
APROBADA
CÁLCULO EN VARIAS VARIABLES (1000006-M)	4	FUND. OPTATIVA	2020-2S Ordinaria	4.1
APROBADA
ECUACIONES DIFERENCIALES (1000007-M)	4	FUND. OPTATIVA	2020-2S Ordinaria	4.6
APROBADA
Fundamentos de programación (3010435)	3	DISCIPLINAR OBLIGATORIA	2020-2S Ordinaria	5.0
APROBADA
ÁLGEBRA LINEAL (1000003-M)	4	FUND. OBLIGATORIA	2019-2S Ordinaria	4.6
APROBADA
CÁLCULO INTEGRAL (1000005-M)	4	FUND. OBLIGATORIA	2019-2S Ordinaria	4.5
APROBADA
FÍSICA MECÁNICA (1000019-M)	4	FUND. OBLIGATORIA	2019-2S Ordinaria	4.7
APROBADA
MATEMÁTICAS DISCRETAS (3006906)	4	FUND. OBLIGATORIA	2019-2S Ordinaria	4.6
APROBADA
CÁLCULO DIFERENCIAL (1000004-M)	4	FUND. OBLIGATORIA	2019-1S Ordinaria	4.7
APROBADA
GEOMETRÍA VECTORIAL Y ANALÍTICA (1000008-M)	4	FUND. OBLIGATORIA	2019-1S Ordinaria	4.8
APROBADA
Introducción a la ingeniería de sistemas e informática (3010438)	2	DISCIPLINAR OBLIGATORIA	2019-1S Ordinaria	4.5
APROBADA
Cátedra Ingenierías Facultad de Minas (3009511)	2	LIBRE ELECCIÓN	2019-1S Ordinaria	4.8
APROBADA
INGLÉS I (1000044-M)	3	NIVELACIÓN	2019-1S Validacion por suficiencia	
APROBADA
INGLÉS II (1000045-M)	3	NIVELACIÓN	2019-1S Validacion por suficiencia	
APROBADA
INGLÉS III (1000046-M)	3	NIVELACIÓN	2019-1S Validacion por suficiencia	
APROBADA
INGLÉS IV (1000047-M)	3	NIVELACIÓN	2019-1S Validacion por suficiencia	
APROBADA

Resumen de créditos
TIPOLOGÍAS
EXIGIDOS
APROBADOS
PENDIENTES
INSCRITOS
CURSADOS
DISCIPLINAR OPTATIVA	22	6	16	6	6
FUND. OBLIGATORIA	27	27	0	0	27
FUND. OPTATIVA	16	12	4	0	12
DISCIPLINAR OBLIGATORIA	57	41	16	3	44
LIBRE ELECCIÓN	32	19	13	3	16
TRABAJO DE GRADO	6	0	6	0	0
TOTAL	160	105	55	12	105
NIVELACIÓN	12	12	0	0	12
TOTAL ESTUDIANTE	172	117	55	12	117


Total Créditos Excedentes3



Total de Créditos Cancelados en los Periodos Cursado0



Porcentaje de Avance65,6%


Cupo de créditos


Cupo de créditos123Créditos adicionales80
Créditos disponibles68
Créditos de estudio doble titulación80


Universidad Nacional de Colombia--Dirección Nacional de Información Académica
Portal de Servicios Académicos (V. 4.3.20) |UXXI Todos los derechos reservados
"""

def obtener_df_materias(historia_academica, periodo: list = None,
                        tipo: list = None):
    # TODO: preguntar como aparecen materias perdidas

    materias_cursadas = str(
        re.search(r'CALIFICACIÓN\n([\S\s]*)\nResumen de créditos',
                  historia_academica).group(1))
    materias_cursadas = re.sub(r'\nAPROBADA|\nREPROBADO', '', materias_cursadas)

    cols_names = ['ASIGNATURAS', 'CREDITOS', 'TIPO', 'PERIODO', 'CALIFICACION']
    materias_cursadas = pd.read_table(StringIO(materias_cursadas), sep='\t',
                                      names=cols_names)

    if periodo is not None:
        # TODO: separar periodo academico y (validaciones o regular)
        materias_cursadas = materias_cursadas[
            materias_cursadas['PERIODO'].isin(periodo)]

    if tipo is not None:
        materias_cursadas = materias_cursadas[
            materias_cursadas['TIPO'].isin(periodo)]
    materias_cursadas = materias_cursadas.astype(str)
    return materias_cursadas.to_dict('records')


@historia.get('/historia', status_code=200)
async def obtener_historia(response: Response):

    """Consulta los id y nombres de las cámaras"""
    success = None
    data = None
    status_code = None
    message = None

    try:
        data = obtener_df_materias(historia_academica)
        status_code = 200
        success = True
        message = 'melo'
    except Exception as e:
        message = 'no melo'
        success = False
        status_code = 500
        data = None
    finally:
        response.status_code = status_code
        res = dict(success=success, msg=message, data=data)

    return res


app.include_router(historia)

if __name__ == '__main__':
    uvicorn.run(app)
