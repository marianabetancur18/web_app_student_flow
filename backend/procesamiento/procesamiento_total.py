import re
import pandas as pd
from io import StringIO

from procesamiento.materias import lista_materias_cursadas
from procesamiento.materias import lista_materias_faltantes
from procesamiento.materias import porcentaje_avance


def procesar_historia(historia_academica: str):

    # TODO: crear cada funcion en un archivo diferente en el que se realice la
    #  extracción de cada parte necesaria para el front

    texto_historia_academica = historia_academica.replace('\r', '')

    patron = r"CALIFICACIÓN\n([\S\s]*)\nResumen de créditos"
    materias_cursadas = str(
        re.search(patron, texto_historia_academica).group(1))
    materias_cursadas = re.sub(r"\nAPROBADA|\nREPROBADO", "", materias_cursadas)

    cols_names = ["ASIGNATURA", "CREDITOS", "TIPO", "PERIODO", "CALIFICACION"]

    # TODO: separar el código de la materia
    materias_cursadas = pd.read_table(
        StringIO(materias_cursadas), sep="\t", names=cols_names
    )

    respuesta = {
        'lista_materias_cursadas': lista_materias_cursadas(materias_cursadas),
        'materias_faltantes': lista_materias_faltantes(materias_cursadas),
        'porcentaje_avance': porcentaje_avance(),

    }

    return respuesta
