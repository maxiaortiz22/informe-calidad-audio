from scipy.signal import butter, sosfilt
import numpy as np
#IMPLEMENTAR UNA FORMA DE GENERAR LOS FILTROS UNA SOLA VEZ PARA OPTIMIZAR LOS CÁLCULOS

class BandpassFilter:

    def __init__(self, type, fs, order, bands):
        self.type = type #str: 'octave band' or 'third octave band' 
        self.fs = fs # int: Frecuencia de sampleo
        self.order = order #int: Orden del filtro
        self.bands = bands #List: Lista de bandas a analizar, ej: [125, 250, 500, 1000, 2000, 4000, 8000]

        # Calculo los parámetros del filtro una única vez al inicializar la clase:
        self.sos = []

        for band in self.bands:
            
            if self.type == 'octave band':
                lowcut = band/np.sqrt(2) #Frecuencia de corte inferior bandas de octava
                highcut = band*np.sqrt(2) #Frecuencia de corte  superior bandas de octava
            elif self.type == 'third octave band':
                lowcut = band/(2**(1/6)) #Frecuencia de corte inferior bandas de tercio de octava
                highcut = band*(2**(1/6)) #Frecuencia de corte  superior bandas de tercio de octava

            self.sos.append(butter(self.order, [lowcut, highcut], fs=self.fs, btype='bandpass', output='sos'))



    def filtered_signals(self, data):

        filtered_audios = np.empty((len(self.bands), len(data))) # Array vacio para cargar las señales filtradas

        for i, sos in enumerate(self.sos):
            filtered_audios[i, :] = sosfilt(sos, data)

        return filtered_audios