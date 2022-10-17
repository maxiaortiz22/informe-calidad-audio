import numpy as np
import pandas as pd
import sys
from scipy.fft import rfft, rfftfreq

#Recomendable: calibrar los tonos a 65 dBHL

def get_compensation(transductor: str) -> list:
    if transductor == 'Supraural (ej: JBL600)':
        return [45, 27, 13.5, 9, 7.5, 7.5, 9, 11.5, 12, 16, 15.5]
    elif transductor == "Circumaural (ej: JBL750)":
        return [30.5, 18, 11, 6,  5.5, 5.5, 4.5, 2.5, 9.5, 17, 17.5]
    elif transductor == 'vincha ósea':
        return [8.4, 9.8, 11.2, 11.6, 13.5, 13.6, 16.3, 25]
    else:
        raise TypeError("No cargaste ningún transductor")

def linealidad_aerea(cal: list[float], data: list[np.ndarray], sr: int, auricular: str) -> pd.DataFrame:
    """Esta función hace el cálculo de linealidad. Primero todo todo el audio grabado y lo
    separo por banda sabiendo cuánto dura la grabación de cada una. Después de eso hago todo el
    calculo de linealidad. Luego tengo que saber cuánto es el máximo y el mínimo de nivel medido
    para crear el cuadro de linealidad"""

    frec = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000] #Frequencies to analyze

    #Creo diccionarios con los audios grabados, la key de cada diccionario es la frecuencia grabada
    audios = {}
    
    i=0
    recorte = int(11*2*sr) #[pasos][segundos_grabacion][sr] = [muestras_por_frecuencia] no sera 12?
    for cal_i, f in enumerate(frec):
        #Separo la data por frecuencia y los calibro a dBSPL:
        audios[str(f)] = data[int(i) : int(i + recorte)] / cal[cal_i] #calibration

        i+=recorte
    
    #Recorto los audios en partes de dos segundos
    i=0
    trimm = {}
    for key in audios.keys():
        n_cut = round(len(audios[key])/(sr*2),0) #cantidad de cortes
        #print(n_cut)
        cut = int(len(audios[key])/n_cut)
        for t in range(0,int(n_cut)):
            i+=1
            trimm[key+'_'+str(i)] = audios[key][int(cut*t) : int(cut*(t+1))] #recorte de dos segundos
            trimm[key+'_'+str(i)] = trimm[key+'_'+str(i)][int(0.5*sr) : int(-0.5*sr)] #testear si funciona
                                                                                      #mejor con este recorte
        i=0

    trimm_global_dB = {'125': [],
                       '250': [],
                       '500': [],
                       '750': [],
                       '1000': [],
                       '1500': [],
                       '2000': [],
                       '3000': [], 
                       '4000': [],
                       '6000': [],
                       '8000': []}

    for key in trimm.keys(): #Guardo el valor de la fft

        # Number of samples in normalized_tone
        N = len(trimm[key])

        # Note the extra 'r' at the front
        yf = np.abs(rfft(trimm[key])) / (N/np.sqrt(2)) #Divido por N/raiz(2) para compensar la amplitud de la fft
        xf = rfftfreq(N, 1 / sr)

        yf_db = 20*np.log10(yf / (20*10**(-6)) + sys.float_info.epsilon)

        idx = np.where(xf == int(key.split('_')[0]))[0]

        trimm_global_dB[key.split('_')[0]].append(yf_db[idx])


    supraural_comp = {'125': 45,
                      '250': 27,
                      '500': 13.5,
                      '750': 9,
                      '1000': 7.5,
                      '1500': 7.5,
                      '2000': 9,
                      '3000': 11.5, 
                      '4000': 12,
                      '6000': 16,
                      '8000': 15.5}

    circumaural_comp = {'125': 30.5,
                        '250': 18,
                        '500': 11,
                        '750': 6,
                        '1000': 5.5,
                        '1500': 5.5,
                        '2000': 4.5,
                        '3000': 2.5, 
                        '4000': 9.5,
                        '6000': 17,
                        '8000': 17.5}

    trimm_global_dB_norm = {}
    aux = []
    for key in trimm_global_dB.keys():
        if auricular == 'Supraural (ej: JBL600)':
            for i in range(len(trimm_global_dB[key])):
                aux.append(np.round_(trimm_global_dB[key][i] - supraural_comp[key])[0])
            trimm_global_dB_norm[key+' Hz'] = aux
        elif auricular == "Circumaural (ej: JBL750)":
            for i in range(len(trimm_global_dB[key])):
                aux.append(np.round_(trimm_global_dB[key][i] - circumaural_comp[key])[0])
            trimm_global_dB_norm[key+' Hz'] = aux
        else:
            raise TypeError("No cargaste ningún auricular")
        
        aux = []

    INDEX = ['40 dBHL', '35 dBHL', '30 dBHL', '25 dBHL', "20 dBHL",
             '15 dBHL', '10 dBHL', '5 dBHL' , '0 dBHL' , "-5 dBHL", "-10 dBHL"]

    test = pd.DataFrame(data=trimm_global_dB_norm, index=INDEX)

    print(test)

    return test

def linealidad_osea(cal: list[float], data: list[np.ndarray], sr: int) -> pd.DataFrame:
    """Esta función hace el cálculo de linealidad. Primero todo todo el audio grabado y lo
    separo por banda sabiendo cuánto dura la grabación de cada una. Después de eso hago todo el
    calculo de linealidad. Luego tengo que saber cuánto es el máximo y el mínimo de nivel medido
    para crear el cuadro de linealidad"""

    frec = [250, 500, 750, 1000, 1500, 2000, 3000, 4000] #Frequencies to analyze

    #Creo diccionarios con los audios grabados, la key de cada diccionario es la frecuencia grabada
    audios = {}
    
    i=0
    recorte = int(9*2*sr) #[pasos][segundos_grabacion][sr] = [muestras_por_frecuencia] 
    for cal_i, f in enumerate(frec):
        #Separo la data por frecuencia y los calibro a dBSPL:
        audios[str(f)] = data[int(i) : int(i + recorte)] / cal[cal_i] #calibration

        i+=recorte
    
    #Recorto los audios en partes de dos segundos
    i=0
    trimm = {}
    for key in audios.keys():
        n_cut = round(len(audios[key])/(sr*2),0) #cantidad de cortes
        #print(n_cut)
        cut = int(len(audios[key])/n_cut)
        for t in range(0,int(n_cut)):
            i+=1
            trimm[key+'_'+str(i)] = audios[key][int(cut*t) : int(cut*(t+1))] #recorte de dos segundos
            trimm[key+'_'+str(i)] = trimm[key+'_'+str(i)][int(0.5*sr) : int(-0.5*sr)] #testear si funciona
                                                                                      #mejor con este recorte
        i=0

    trimm_global_dB = {'250': [],
                       '500': [],
                       '750': [],
                       '1000': [],
                       '1500': [],
                       '2000': [],
                       '3000': [], 
                       '4000': []}

    for key in trimm.keys(): #Guardo el valor de la fft

        # Number of samples in normalized_tone
        N = len(trimm[key])

        # Note the extra 'r' at the front
        yf = np.abs(rfft(trimm[key])) / (N/np.sqrt(2)) #Divido por N/raiz(2) para compensar la amplitud de la fft
        xf = rfftfreq(N, 1 / sr)

        yf_db = 20*np.log10(yf / (20*10**(-6)) + sys.float_info.epsilon)

        idx = np.where(xf == int(key.split('_')[0]))[0]

        trimm_global_dB[key.split('_')[0]].append(yf_db[idx])

    
    osea_comp = {'250': 8.4,
                 '500': 9.8,
                 '750': 11.2,
                 '1000': 11.6,
                 '1500': 13.5,
                 '2000': 13.6,
                 '3000': 16.3, 
                 '4000': 25}

    trimm_global_dB_norm = {}
    aux = []
    for key in trimm_global_dB.keys():

        for i in range(len(trimm_global_dB[key])):
            aux.append(np.round_(trimm_global_dB[key][i] - osea_comp[key])[0])
        trimm_global_dB_norm[key+' Hz'] = aux
        
        aux = []

    INDEX = ['30 dBHL', '25 dBHL', "20 dBHL", '15 dBHL', '10 dBHL', '5 dBHL', '0 dBHL', "-5 dBHL", "-10 dBHL"]

    test = pd.DataFrame(data=trimm_global_dB_norm, index=INDEX)

    print(test)

    return test