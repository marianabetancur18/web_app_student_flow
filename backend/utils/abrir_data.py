import pandas as pd
import os


def obtener_pensum() -> pd.DataFrame:
    """Obtiene el pensum completo de la historia

    Returns:
        un DataFrame con las columnas
    """

    ruta_historia = os.path.join('files', 'pensum.csv')
    pensum = pd.read_csv(ruta_historia)

    return pensum
