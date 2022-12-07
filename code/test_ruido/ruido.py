import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
from scipy.fft import rfft, rfftfreq
import pandas as pd

def get_ruido(data: list[np.ndarray], cal: float, sr: float, auricular: str) -> pd.DataFrame:

    ruidos = [ruido/cal for ruido in data]

    if auricular == 'Supraural (ej: JBL600)':
        comp = [20, 20, 13.5]
    elif auricular == "Circumaural (ej: JBL750)":
        comp = [20, 20, 11.5]

    niveles = list(map(lambda x: np.round(20*np.log10(np.sqrt(np.mean(x**2)) / (20*10**(-6)) + sys.float_info.epsilon), 2), ruidos))

    niveles = [np.round(niveles[i] - val, 2) for i, val in enumerate(comp)]

    ruidos_dB = []
    for ruido in ruidos:
        N = len(ruido)

        yf = np.abs(np.array(rfft(ruido))) / (N/np.sqrt(2)) #Divido por N/raiz(2) para compensar la amplitud de la fft
        xf = rfftfreq(N, 1 / sr)

        yf_db = 20*np.log10(yf / (20*10**(-6)) + sys.float_info.epsilon)

        ruidos_dB.append([xf, yf_db])
    
    noise_types = ['Ruido blanco', 'Ruido vocal', 'NBN 1kHz']
    ftick = [20, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
    labels = ['20', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k', '20k']

    plt.cla()
    plt.clf()

    for i, noise_type in enumerate(noise_types):
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(ruidos_dB[i][0], ruidos_dB[i][1], label=noise_type)
        ax.set_title(label=noise_type)
        ax.set_xlabel('Frecuencia [Hz]', color='black')
        ax.set_ylabel('Nivel [dBSPL]', color='black')
        ax.set_xscale('log')
        ax.set_xticks(ftick)
        ax.set_xticklabels(labels, rotation=90)
        ax.set_xlim(20, 20000)
        ax.legend()
        plt.tight_layout()

        plt.savefig(f'results/test_images/{noise_type}.png')

    data_ = {'Tipo': noise_types,'Nivel [dBHL]': niveles}

    df = pd.DataFrame(data=data_)

    print(df)
    
    return df