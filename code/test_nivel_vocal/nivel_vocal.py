import numpy as np
import pandas as pd
import sys

def get_nivel_vocal(data: list[np.ndarray], cal: float) -> pd.DataFrame:
    """Para este test se grabaran a 85 dBHL el conjunto de palabras sin silencio de las
    listas:
    
    * Dr. Tato adultos
    * Dr. Tato niños
    * SRT E IRF (masculino)
    * SRT E IRF (femenino)
    * Audicom
    """

    audios_calibrados = [record/cal for record in data] #Calibro los audios

    nivel_vocal = list(map(lambda x: np.round(20*np.log10(np.sqrt(np.mean(x**2)) / (20*10**(-6)) + sys.float_info.epsilon) - 20, 2), audios_calibrados))

    LISTAS = ['Dr. Tato adultos', 'Dr. Tato niños', "SRT E IRF (masculino)", 
             'SRT E IRF (femenino)', 'Audicom']

    data_ = {'Lista': LISTAS, 'Nivel vocal [dBHL]': nivel_vocal}
    

    df = pd.DataFrame(data=data_)

    print(df)

    return df