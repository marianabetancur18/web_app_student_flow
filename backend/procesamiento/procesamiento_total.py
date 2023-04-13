from procesamiento.materias import lista_materias_cursadas


def procesar_historia(historia_academica: str, argumentos: dict):

    # TODO: crear cada funcion en un archivo diferente en el que se realice la
    #  extracción de cada parte necesaria para el front
    respuesta = {
        'lista_materias_cursadas': lista_materias_cursadas(historia_academica)
    }

    return respuesta