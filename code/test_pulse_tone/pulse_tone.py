import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
import pandas as pd

def get_pulse_tone(data: np.ndarray, sr: int) -> pd.DataFrame:
    #Genero el test:

    data = data/np.max(np.abs(data))

    tono = np.abs(hilbert(data))

    DISTANCE = sr*192*(10**(-3)) #Espero que la distancia entre los picos sea mayor a 192ms (on-time del tono pulsante)

    local_max_idx, _ = find_peaks(tono, height=0.5, distance=DISTANCE)

    #Recorto el tono en el segundo y tercer pulso:
    first_max = local_max_idx[1]
    second_max = local_max_idx[2]

    end_left = np.where(np.flip(tono[:first_max])<=tono[first_max]*0.1)[0][0]
    end_left = first_max - end_left

    end_right = np.where(tono[second_max:]<=tono[second_max]*0.1)[0][0]
    end_right = second_max + end_right

    tono = tono[(end_left-2000):(end_right+2000)]

    #Busco los tiempos de los pulsos:
    local_max_idx, _ = find_peaks(tono, height=0.5, distance=DISTANCE)

    first_max = local_max_idx[0]
    second_max = local_max_idx[1]

    #Tiempos del primer ciclo:
    first_rise_min_left = np.where(np.flip(tono[:first_max])<=tono[first_max]*0.1)[0][0]
    first_rise_min_left = first_max - first_rise_min_left
    
    first_rise_max_left = np.where(np.flip(tono[:first_max])<=tono[first_max]*0.9)[0][0]
    first_rise_max_left = first_max - first_rise_max_left

    first_fall_min_left = np.where(tono[first_max:]<=tono[first_max]*0.1)[0][0]
    first_fall_min_left = first_max + first_fall_min_left

    first_fall_middle_left = np.where(tono[first_max:]<=tono[first_max]*0.5)[0][0]
    first_fall_middle_left = first_max + first_fall_middle_left

    first_fall_max_left = np.where(tono[first_max:]<=tono[first_max]*0.9)[0][0]
    first_fall_max_left = first_max + first_fall_max_left

    #Tiempos del segundo ciclo:
    second_rise_min_left = np.where(np.flip(tono[:second_max])<=tono[second_max]*0.1)[0][0]
    second_rise_min_left = second_max - second_rise_min_left
    
    second_rise_middle_left = np.where(np.flip(tono[:second_max])<=tono[second_max]*0.5)[0][0]
    second_rise_middle_left = second_max - second_rise_middle_left

    print(f'Rise time: {((first_rise_max_left-first_rise_min_left)/sr)*10**3} ms')
    print(f'Fall time: {((first_fall_min_left-first_fall_max_left)/sr)*10**3} ms')
    print(f'On time: {((first_fall_max_left-first_rise_max_left)/sr)*10**3} ms')
    print(f'On/Off time: {((second_rise_middle_left-first_fall_middle_left)/sr)*10**3} ms')

    times = {'Rise time [ms]': np.round(((first_rise_max_left-first_rise_min_left)/sr)*10**3, 2),
             'Fall time [ms]': np.round(((first_fall_min_left-first_fall_max_left)/sr)*10**3, 2),
             'On time [ms]': np.round(((first_fall_max_left-first_rise_max_left)/sr)*10**3, 2),
             'On/Off time [ms]': np.round(((second_rise_middle_left-first_fall_middle_left)/sr)*10**3, 2)}
    
    data_ = {'Tiempos [ms]': ['Rise time', 'Fall time', 'On time', 'On/Off time'],
             'Resultado': [times['Rise time [ms]'], times['Fall time [ms]'], times['On time [ms]'], times['On/Off time [ms]']]}
    
    plt.cla()
    plt.clf()

    #plt.rcParams["figure.figsize"] = (5,4)

    #plt.plot(tono)
    fig, ax = plt.subplots(figsize=(5, 4))

    ax.plot(tono)
    
    for idx in [first_rise_min_left, first_rise_max_left, first_fall_min_left, 
                first_fall_middle_left, first_fall_max_left, second_rise_min_left, second_rise_middle_left]:

        ax.vlines(x = idx, ymin = min(tono), ymax = max(tono), colors = 'purple')

    plt.tight_layout()
    
    plt.savefig('results/test_images/pulse_tone.png')

    df = pd.DataFrame(data=data_)

    return df