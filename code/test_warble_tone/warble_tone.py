from scipy.fft import rfft, rfftfreq
import numpy as np
from scipy.signal import find_peaks
import pandas as pd

class FcError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'FcError: {self.message}'
        else:
            return 'FcError: no se encontró la frecuencia de mensaje'

def get_frec_mod(data: list[np.ndarray], fs: float) -> pd.DataFrame:

    frecs = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    fc, fm = [], []

    assert(len(data) == len(frecs))

    for i, audio in enumerate(data):

        audio = audio / np.max(np.abs(audio))
        
        N = len(audio)
        yf = np.array(rfft(audio))
        xf = rfftfreq(N, 1 / fs)

        yf = 20 * np.log10(np.abs(yf) / np.max(np.abs(yf)))

        local_max_idx, _ = find_peaks(yf, height=-15) #Revisar el valor de height

        xf_max_list = [xf[i] for i in local_max_idx]

        fm_calc = []
        for t in range(len(xf_max_list)-1):
            fm_calc.append(xf_max_list[t+1]-xf_max_list[t])

        fm_calc = np.min(list(set(fm_calc)))#[0] #ESTO ESTÁ FUNCIONANDO MAL, VA A HABER QUE HACER UN CAMBIO Y QUEDARSE SOLO CON LAS CERCANAS A LA BANDA EN CUESTIÓN, SINO TOMA OTROS SALTOS!!!!

        check_fc = map(lambda frec: frec == frecs[i], xf_max_list)

        if any(check_fc):
            fc.append(frecs[i])
        
        else:
            #raise FcError(f'no se encontró la frecuencia de mensaje de {frecs[i]} Hz')
            fc.append(np.nan)
        
        fm.append(fm_calc)

    data_df = {'Carrier frequency [Hz]': fc,
               'Modulating frequency [Hz]': fm}

    df = pd.DataFrame(data_df)

    print(df)

    return df