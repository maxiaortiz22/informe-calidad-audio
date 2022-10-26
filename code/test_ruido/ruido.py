import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
from scipy.fft import rfft, rfftfreq
import pandas as pd

def get_ruido(data: list[np.ndarray], cal: float, sr: float) -> pd.DataFrame:
    
    ruidos = [ruido/cal for ruido in data]

    niveles = list(map(lambda x: np.sqrt(np.mean(x**2)), ruidos))

    ruidos_dB = []
    for ruido in ruidos:
        N = len(ruido)

        yf = np.abs(np.array(rfft(ruido))) / (N/np.sqrt(2)) #Divido por N/raiz(2) para compensar la amplitud de la fft
        xf = rfftfreq(N, 1 / sr)

        yf_db = 20*np.log10(yf / (20*10**(-6)) + sys.float_info.epsilon)

        ruidos_dB.append([xf, yf_db])
    
    noise_types = ['Ruido blanco', 'Ruido vocal', 'NBN 1kHz']

    for i, noise_type in enumerate(noise_types):
        fig, ax = plt.subplots()
        ax.plot(ruidos_dB[i][0], ruidos_dB[i][1], label=noise_type)
        ax.set_xlabel('Frecuencia [Hz]', color='black')
        ax.set_ylabel('Nivel [dBSPL]', color='black')
        ax.set_xlim(20, 20000)
        ax.legend()
        plt.tight_layout()

        plt.savefig(f'test_images/{noise_type}.png')

    data_ = {'Nivel [dBSPL]': niveles}

    df = pd.DataFrame(data=data_, index=noise_types)

    print(df)
    
    return df
        
    


