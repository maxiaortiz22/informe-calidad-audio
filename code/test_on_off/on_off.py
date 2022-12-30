import numpy as np
import pandas as pd
from scipy.signal import hilbert
import matplotlib.pyplot as plt

def get_on_off_time(data: np.ndarray, sr: int) -> pd.DataFrame:

    """La idea de este test es grabar 5 segundos de audio, en los cuales
    voy a tener que encender y apagar el tono para ver cuánto tiempo tarda en
    pasar de cero al máximo de señal y viceversa"""

    data = data/np.max(np.abs(data))
    tono = np.abs(hilbert(data))

    max_idx = [i for i in range(len(tono)) if tono[i] == np.max(tono)][0]

    #Encuentro los índices para el cálculo del tiempo de encendido y apagado:
    end_left = np.where(np.flip(tono[:max_idx])<=tono[max_idx]*0.1)[0][0]
    end_left = max_idx - end_left

    end_right = np.where(tono[max_idx:]<=tono[max_idx]*0.1)[0][0]
    end_right = max_idx + end_right

    max_left = np.where(np.flip(tono[:max_idx])<=tono[max_idx]*0.9)[0][0]
    max_left = max_idx - max_left

    max_right = np.where(tono[max_idx:]<=tono[max_idx]*0.9)[0][0]
    max_right = max_idx + max_right

    #Recorto el tono:
    tono = tono[(end_left-1000):(end_right+1000)]

    #Vuelvo a calcular los índices:

    max_idx = [i for i in range(len(tono)) if tono[i] == np.max(tono)][0]

    end_left = np.where(np.flip(tono[:max_idx])<=tono[max_idx]*0.1)[0][0]
    end_left = max_idx - end_left

    end_right = np.where(tono[max_idx:]<=tono[max_idx]*0.1)[0][0]
    end_right = max_idx + end_right

    max_left = np.where(np.flip(tono[:max_idx])<=tono[max_idx]*0.9)[0][0]
    max_left = max_idx - max_left

    max_right = np.where(tono[max_idx:]<=tono[max_idx]*0.9)[0][0]
    max_right = max_idx + max_right

    #Calculo los tiempos:
    print(f'On time: {((max_left-end_left)/sr)*10**3} ms')
    print(f'Off time: {((end_right-max_right)/sr)*10**3} ms')

    times = {'On time [ms]': np.round(((max_left-end_left)/sr)*10**3, 2),
             'Off time [ms]': np.round(((end_right-max_right)/sr)*10**3, 2)}

    data_ = {'Tiempos [ms]': ['On time', 'Off time'],
             'Resultado': [times['On time [ms]'], times['Off time [ms]']]}

    plt.cla()
    plt.clf()

    #plt.rcParams["figure.figsize"] = (5,3)

    #plt.plot(tono)
    fig, ax = plt.subplots(figsize=(5, 4))

    ax.plot(tono)
    
    for idx in [end_left, end_right, max_left, max_right]:

        ax.vlines(x = idx, ymin = min(tono), ymax = max(tono), colors = 'purple')

    plt.savefig('results/test_images/on_off_tono.png')

    df = pd.DataFrame(data=data_)

    return df