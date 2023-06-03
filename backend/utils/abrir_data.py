import pandas as pd
import os


def obtener_pensum() -> pd.DataFrame:
    """Obtiene el pensum completo de la historia

    Returns:
        un DataFrame con las columnas ['CODIGO', 'NOMBRE', 'CREDITOS', 'TIPO', 'PRERREQUISITOS']
    """
    ruta_historia = os.path.join(os.getcwd(), 'backend', 'files', 'pensum.csv')
    pensum = pd.read_csv(ruta_historia)

    return pensum
