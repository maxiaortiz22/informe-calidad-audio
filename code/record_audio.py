import numpy as np

def RMS(y):
    """ Calcula el valor RMS de una señal """
    rms = np.sqrt(np.mean(y**2))
    #rms=np.mean(y**2)
    return rms

def RMS_cal(y, nivel_dBHL, comp):
    """ Calcula el valor RMS de una señal de calibración de cualquier nivel y lo paso a 94 dBSPL,
        lo que equivale a 1 Pa """

    rms = np.sqrt(np.mean(y**2)) #Obento el RMS al nivel que fue grabado

    rms_1Pa = rms / (20*10**(-6) * 10**((nivel_dBHL+comp)/20)) #Paso le RMS a 1 Pa
    
    return rms_1Pa