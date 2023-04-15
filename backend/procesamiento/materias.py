import pandas as pd
import re
from io import StringIO

from utils.abrir_data import obtener_pensum


def crear_df_materias_cursadas(texto_historia_academica: str) -> pd.DataFrame:
    """Crea una tabla con las materias cursadas

    Returns:
        DataFrame con columnas ["CREDITOS", "TIPO", "PERIODO", "CALIFICACION"]

    """
    texto_historia_academica = texto_historia_academica.replace('\r', '')

    patron = r"CALIFICACIÓN\n([\S\s]*)\nResumen de créditos"
    materias_cursadas = str(
        re.search(patron, texto_historia_academica).group(1))
    materias_cursadas = re.sub(r"\nAPROBADA|\nREPROBADO", "", materias_cursadas)

    cols_names = ["NOMBRE-CODIGO", "CREDITOS", "TIPO", "PERIODO",
                  "CALIFICACION"]

    materias_cursadas = pd.read_table(
        StringIO(materias_cursadas), sep="\t", names=cols_names
    )

    materias_cursadas[['NOMBRE', 'CODIGO']] = materias_cursadas[
        'NOMBRE-CODIGO'].str.split('(', expand=True)

    materias_cursadas.drop('NOMBRE-CODIGO', axis=1, inplace=True)

    materias_cursadas['NOMBRE'] = materias_cursadas['NOMBRE'].str.strip()
    materias_cursadas['NOMBRE'] = materias_cursadas['NOMBRE'].str.strip('(')
    materias_cursadas['CODIGO'] = materias_cursadas['CODIGO'].str.replace(')', '')

    return materias_cursadas


def lista_materias_cursadas(
        materias_cursadas: pd.DataFrame,
        periodo: list = None,
        tipo: list = None) -> list:

    """
    Obtiene una lista de las materias cursadas a partir del texto obtenido del
     ctrl+a en el sia.

    Args:
        materias_cursadas: contiene las materias cursadas
        periodo: periodo académico en caso de que se desee filtrar
        tipo: tipo de materia en caso de que se quiera fitlrar

    Returns:
        .. code-block:: python

            [
                {
                    'ASIGNATURA': 'Desarrollo Web',
                    'CREDITOS': '3',
                    'TIPO': 'Disciplinar obligatoria',
                    'PERIODO': '2022-2',
                    'CALIFICACION': '4.5'
                },
                {
                    'ASIGNATURA': 'Ingeniería de requisitos',
                    'CREDITOS': '3',
                    'TIPO': 'Disciplinar obligatoria',
                    'PERIODO': '2022-2',
                    'CALIFICACION': '5.0'
                },
            ]

    """

    if periodo is not None:
        # TODO: separar periodo academico y (validaciones o regular)
        materias_cursadas = materias_cursadas[
            materias_cursadas["PERIODO"].isin(periodo)
        ]

    if tipo is not None:
        materias_cursadas = materias_cursadas[
            materias_cursadas["TIPO"].isin(periodo)]

    materias_cursadas = materias_cursadas.astype(str)
    lista_materias_cursadas = materias_cursadas.to_dict("records")

    return lista_materias_cursadas


def lista_materias_faltantes(
        materias_cursadas: pd.DataFrame,
        periodo: list = None,
        tipo: list = None) -> list:

    """
    Obtiene una lista de las materias faltantes a partir del texto obtenido del
     ctrl+a en el sia.

    Args:
        materias_cursadas: contiene las materias cursadas
        periodo: periodo académico en caso de que se desee filtrar
        tipo: tipo de materia en caso de que se quiera fitlrar

    Returns:
        .. code-block:: python

            [
                {
                    'ASIGNATURA': 'Desarrollo Web',
                    'CREDITOS': '3',
                    'TIPO': 'Disciplinar obligatoria'
                },
                {
                    'ASIGNATURA': 'Ingeniería de requisitos',
                    'CREDITOS': '3',
                    'TIPO': 'Disciplinar obligatoria'
                },
            ]

    """

    pensum = obtener_pensum()

    pass


def porcentaje_avance(materias_cursadas: pd.DataFrame):
    """
    Obtiene el porcentaje por tipología de materia.

    Returns:
        .. code-block:: python
        {
            "avance_disciplinar_total": "58 %",
            "avance_disciplinar_optativa": "49,5 %",
            "avance_disciplinar_obligatoria": "32 %",
            "avance_fundamentacion_total": "51 %",
            "avance_fundamentacion_obligatoria": "7 %",
            "avance_fundamentacion_optatativa": "4 %"
        }

    """

    pensum = obtener_pensum()

    pass


def estimado_semestres_faltantes(materias_cursadas: pd.DataFrame) -> str:
    """Calcula la cantidad de semestres faltantes basandose en un promedio de
     materias o créditos vistos por semestre

    Args:
        materias_cursadas:

    Returns:
        Cantidad de semestres faltantes.

    """
    pensum = obtener_pensum()
    semestres_cursados = len(materias_cursadas['PERIODO'].unique()) - 1 # Se resta uno porque sale este semestre  
    creditos_cursados = materias_cursadas['CREDITOS'].sum(axis = 0)
    promedio_creditos = creditos_cursados / semestres_cursados
    creditos_pensum = 168
    creditos_faltantes = creditos_pensum - creditos_cursados
    semestres_faltantes = str(int(creditos_faltantes/promedio_creditos))
    return semestres_faltantes
 


