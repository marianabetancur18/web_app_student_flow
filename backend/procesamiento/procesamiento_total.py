

from procesamiento.materias import lista_materias_cursadas
from procesamiento.materias import lista_materias_faltantes
from procesamiento.materias import porcentaje_avance
from procesamiento.materias import crear_df_materias_cursadas
from procesamiento.materias import estimado_semestres_faltantes
from procesamiento.materias import grafo_materias_cursadas
from procesamiento.materias import grafo_pensum


def procesar_historia(historia_academica: str):

    materias_cursadas = crear_df_materias_cursadas(historia_academica)

    respuesta = {
        'lista_materias_cursadas': lista_materias_cursadas(materias_cursadas),
        'materias_faltantes': lista_materias_faltantes(materias_cursadas),
        'porcentaje_avance': porcentaje_avance(materias_cursadas),
        'estimado_semestres_faltantes': estimado_semestres_faltantes(materias_cursadas),
        'grafo_materias_cursadas': grafo_materias_cursadas(materias_cursadas),
        'grafo_pensum': grafo_pensum()
    }

    return respuesta
