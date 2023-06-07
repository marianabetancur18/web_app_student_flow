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

    codigos_materias_cursadas = materias_cursadas['CODIGO']
    faltantes = pensum[~pensum['CODIGO'].isin(codigos_materias_cursadas)]
    faltantes_obligatorias = faltantes[
        faltantes['TIPO'].str.contains('OBLIGATORIA')].astype('str').to_dict('records')

    faltantes_optativas = faltantes[
        faltantes['TIPO'].str.contains('OPTATIVA')].astype('str').to_dict('records')

    faltantes = {
        'faltantes_obligatorias': faltantes_obligatorias,
        'faltantes_optativas': faltantes_optativas
    }

    return faltantes


def porcentaje_avance(materias_cursadas: pd.DataFrame):
    """

    Obtiene el porcentaje por tipología de materia.


    args:
        DataFrame con columnas ["CREDITOS", "TIPO", "PERIODO", "CALIFICACION"]


    Returns:
        .. code-block:: python
        {
            "avance_componente_disciplinar:"58.0 %",
            "avance_disciplinar_total": "58.0 %",
            "avance_disciplinar_optativa": "49.5 %",
            "avance_disciplinar_obligatoria": "32.0 %",
            "avance_fundamentacion_total": "51.0 %",
            "avance_fundamentacion_obligatoria": "7.0 %",
            "avance_fundamentacion_optativa": "4.0 %",
            "avance_libre_eleccion_total": "4.0 %"
        }

    """

    PENSUM_DISCIPLINAR_OBLIGATORIA=63-6
    PENSUM_DISCIPLINAR_OPTATIVA=22
    PENSUM_DISCIPLINAR_TOTAL=PENSUM_DISCIPLINAR_OPTATIVA+PENSUM_DISCIPLINAR_OBLIGATORIA

    PENSUM_TRABAJO_GRADO=6
    PENSUM_COMPONENTE_DISCIPLINAR=PENSUM_DISCIPLINAR_TOTAL+PENSUM_TRABAJO_GRADO


    PENSUM_FUDAMENTACION_OBLIGATORIA=27
    PENSUM_FUDAMENTACION_OPTATIVA=16
    PENSUM_FUNDAMENTACION_TOTAL=PENSUM_FUDAMENTACION_OPTATIVA+PENSUM_FUDAMENTACION_OBLIGATORIA

    PENSUM_LIBRE_ELECCION_TOTAL=32

    PENSUM_CARRERA_TOTAL=PENSUM_LIBRE_ELECCION_TOTAL+PENSUM_COMPONENTE_DISCIPLINAR+PENSUM_FUNDAMENTACION_TOTAL

    creditos_cursados_libre_eleccion_total=materias_cursadas[materias_cursadas["TIPO"]=="LIBRE ELECCIÓN"]["CREDITOS"].sum(axis=0)

    creditos_cursados_disciplinar_optativa=materias_cursadas[materias_cursadas["TIPO"]=="DISCIPLINAR OPTATIVA"]["CREDITOS"].sum(axis=0)
    creditos_cursados_disciplinar_obligatoria=materias_cursadas[materias_cursadas["TIPO"]=="DISCIPLINAR OBLIGATORIA"]["CREDITOS"].sum(axis=0)
    creditos_cursados_disciplinar_total = creditos_cursados_disciplinar_obligatoria + creditos_cursados_disciplinar_optativa


    creditos_cursados_fundamentacion_obligatoria =materias_cursadas[materias_cursadas["TIPO"]=="FUND. OBLIGATORIA"]["CREDITOS"].sum(axis=0)
    creditos_cursados_fundamentacion_optativa =materias_cursadas[materias_cursadas["TIPO"]=="FUND. OPTATIVA"]["CREDITOS"].sum(axis=0)
    creditos_cursados_fundamentacion_total = creditos_cursados_fundamentacion_obligatoria + creditos_cursados_fundamentacion_optativa

    creditos_cursados_trabajo_grado=materias_cursadas[materias_cursadas["TIPO"]=="TRABAJO GRADO"]["CREDITOS"].sum(axis=0)

    creditos_cursados_componente_disciplinar= creditos_cursados_trabajo_grado + creditos_cursados_disciplinar_total

    creditos_cursados_carrera_total= creditos_cursados_fundamentacion_total + creditos_cursados_componente_disciplinar + creditos_cursados_libre_eleccion_total


    calculo_porcentaje_avance = lambda cursado, en_pensum: f'{round(cursado*100/en_pensum,1)} %'



    porcentajes_de_avance ={
        "avance_componente_disciplinar":calculo_porcentaje_avance(creditos_cursados_componente_disciplinar,PENSUM_COMPONENTE_DISCIPLINAR),

        "avance_disciplinar_total": calculo_porcentaje_avance(creditos_cursados_disciplinar_total,PENSUM_DISCIPLINAR_TOTAL),
        "avance_disciplinar_optativa": calculo_porcentaje_avance(creditos_cursados_disciplinar_optativa,PENSUM_DISCIPLINAR_OPTATIVA),
        "avance_disciplinar_obligatoria": calculo_porcentaje_avance(creditos_cursados_disciplinar_obligatoria,PENSUM_DISCIPLINAR_OBLIGATORIA),

        "avance_fundamentacion_total": calculo_porcentaje_avance(creditos_cursados_fundamentacion_total,PENSUM_FUNDAMENTACION_TOTAL),
        "avance_fundamentacion_obligatoria": calculo_porcentaje_avance(creditos_cursados_fundamentacion_obligatoria,PENSUM_FUDAMENTACION_OBLIGATORIA),
        "avance_fundamentacion_optativa": calculo_porcentaje_avance(creditos_cursados_fundamentacion_optativa,PENSUM_FUDAMENTACION_OPTATIVA),

        "avance_libre_eleccion_total": calculo_porcentaje_avance(creditos_cursados_libre_eleccion_total,PENSUM_LIBRE_ELECCION_TOTAL),

        "avance_total_carrera": calculo_porcentaje_avance(creditos_cursados_carrera_total,PENSUM_CARRERA_TOTAL)
    }

    return porcentajes_de_avance


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


def grafo_materias_cursadas(materias_cursadas: pd.DataFrame) -> dict:
    pensum = obtener_pensum()

    # requesitos
    requesitos = pd.merge(
        materias_cursadas[['CODIGO']],
        pensum[['CODIGO', 'PRERREQUISITOS']],
        on='CODIGO')

    requesitos_lista = []
    id_ = 1

    for index, row in requesitos.iterrows():
        prerrequisitos = row['PRERREQUISITOS'].strip('][').split(', ')

        if prerrequisitos == ['']:
            prerrequisitos = []

        for i in prerrequisitos:
            requesitos_lista.append({"id": f'e{id_}', "source": row['CODIGO'],
                                     "target": i.strip('\''),
                                     "type": "smoothstep", "animated": True})
            id_ += 1

    # materias

    materias_lista = []
    for index, row in materias_cursadas.iterrows():
        materias_lista.append(
            {"id": row['CODIGO'], "data": {"label": row['NOMBRE']}})

    grafo = {
        "materias": materias_lista,
        "requisitos": requesitos_lista
    }

    return grafo


def grafo_pensum(materias_cursadas) -> dict:
    pensum = obtener_pensum()

    # requesitos
    requesitos = pensum[['CODIGO', 'PRERREQUISITOS']]

    requesitos_lista = []
    id_ = 1

    for index, row in requesitos.iterrows():
        prerrequisitos = row['PRERREQUISITOS'].strip('][').split(', ')

        if prerrequisitos == ['']:
            prerrequisitos = []

        for i in prerrequisitos:
            requesitos_lista.append({"id": f'e{id_}', "source": i.strip('\''),
                                     "target": row['CODIGO'],
                                     "type": "smoothstep", "animated": True})
            id_ += 1

    materias_cursadas['CURSADA'] = True
    # materias

    grafo = pd.merge(
        pensum[['CODIGO', 'PRERREQUISITOS', 'NOMBRE', 'TIPO']],
        materias_cursadas[['CODIGO', 'CURSADA']],
        on='CODIGO',
        how='left').fillna(False)

    style = {
        (False, False): '#808080',
        (False, True): '#ff2e2e',
        (True, True): '#81F79F',
        (True, False): '#81F79F'
    }

    grafo['OBLIGATORIA'] = grafo['TIPO'].str.contains('OBLIGATORIA')
    grafo['style'] = grafo[['CURSADA', 'OBLIGATORIA']].apply(tuple, axis=1)
    grafo['style'] = grafo['style'].map(style)

    materias_lista = []
    for index, row in grafo.iterrows():
        materias_lista.append(
            {
                "id": row['CODIGO'],
                "data": {"label": row['NOMBRE']},
                "style": {'backgroundColor': row['style']}
            }
        )

    grafo = {
        "materias": materias_lista,
        "requisitos": requesitos_lista
    }

    return grafo
