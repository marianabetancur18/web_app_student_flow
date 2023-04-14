import pandas as pd
import os


def obtener_pensum():
    """Obtiene el pensum completo de la historia"""
    ruta_historia = os.path.join('files', 'historia_academica.csv')
    pensum = pd.read_csv(ruta_historia)

    return pensum
