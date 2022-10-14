import numpy as np
import pandas as pd

def get_nivel_vocal(data: list, cal: float) -> pd.DataFrame:
    """Dada una lista con las grabaciones, calcular el nivel vocal del archivo."""

    nivel_vocal = [record/cal for record in data] #Chequear que record sea un np.array
