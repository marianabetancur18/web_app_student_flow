from procesamiento.materias import lista_materias_cursadas
from procesamiento.materias import lista_materias_faltantes


def procesar_historia(historia_academica: str):

    # TODO: crear cada funcion en un archivo diferente en el que se realice la
    #  extracción de cada parte necesaria para el front
    respuesta = {
        'lista_materias_cursadas': lista_materias_cursadas(historia_academica),
        'materias_faltantes': lista_materias_faltantes(historia_academica)
    }

    return respuesta