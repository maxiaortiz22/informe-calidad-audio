import numpy as np
import pandas as pd

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

    nivel_vocal = list(map(lambda x: np.sqrt(np.mean(x**2)) - 20, audios_calibrados))

    data_ = {'Nivel vocal [dBHL]': nivel_vocal}
    
    INDEX = ['Dr. Tato adultos', 'Dr. Tato niños', "SRT E IRF (masculino)", 
             'SRT E IRF (femenino)', 'Audicom']

    df = pd.DataFrame(data=data_, index=INDEX)

    print(df)

    return df