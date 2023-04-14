import pandas as pd

from utils.abrir_data import obtener_pensum


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
