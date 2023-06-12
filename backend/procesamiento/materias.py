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

    vistos = materias_cursadas.groupby('TIPO', as_index=False).agg(
        creditos_vistos=('CREDITOS', sum))

    necesarios = pd.DataFrame(
        [{'TIPO': 'DISCIPLINAR OBLIGATORIA', 'creditos_necesarios': 57},
         {'TIPO': 'DISCIPLINAR OPTATIVA', 'creditos_necesarios': 22},
         {'TIPO': 'FUND. OBLIGATORIA', 'creditos_necesarios': 27},
         {'TIPO': 'FUND. OPTATIVA', 'creditos_necesarios': 16},
         {'TIPO': 'LIBRE ELECCIÓN', 'creditos_necesarios': 32},
         {'TIPO': 'NIVELACIÓN', 'creditos_necesarios': 12}])

    total = pd.merge(
        vistos,
        necesarios,
        on='TIPO'
    )

    filtro = total['TIPO'].isin(
        ['DISCIPLINAR OBLIGATORIA', 'DISCIPLINAR OPTATIVA'])
    disciplinar_total = total[filtro].copy()

    # Crear una nueva fila con el tipo "DISCIPLINAR TOTAL" y sumar los valores de las columnas numéricas
    disciplinar_total = {
        'TIPO': 'DISCIPLINAR TOTAL',
        'creditos_vistos': disciplinar_total['creditos_vistos'].sum(),
        'creditos_necesarios': disciplinar_total['creditos_necesarios'].sum()
    }

    filtro = total['TIPO'].isin(['FUND. OBLIGATORIA', 'FUND. OPTATIVA'])
    fund_total = total[filtro].copy()

    # Crear una nueva fila con el tipo "DISCIPLINAR TOTAL" y sumar los valores de las columnas numéricas
    fund_total = {
        'TIPO': 'FUND. TOTAL',
        'creditos_vistos': fund_total['creditos_vistos'].sum(),
        'creditos_necesarios': fund_total['creditos_necesarios'].sum()
    }

    # Agregar la nueva fila al DataFrame
    total = pd.concat([total, pd.DataFrame([fund_total, disciplinar_total])])

    total['creditos_faltantes'] = total['creditos_necesarios'] - total[
        'creditos_vistos']
    total['porcentaje_visto'] = round(
        total['creditos_vistos'] * 100 / total['creditos_necesarios'], 2)
    total['porcentaje_faltante'] = round(100 - total['porcentaje_visto'], 2)
    total['porcentaje_faltante'] = total['porcentaje_faltante'].astype(
        str) + ' %'
    total['porcentaje_visto'] = total['porcentaje_visto'].astype(str) + ' %'

    return total.to_dict('records')


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
