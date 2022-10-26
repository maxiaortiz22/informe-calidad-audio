import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import fftconvolve

def sinesweep(f_inf: int = 20, 
              f_sup: int = 20000, 
              T: int = 5, 
              Fs: int = 44100, 
              A: float = 1.0, 
              P: int = 3) -> tuple[np.ndarray, np.ndarray, int, int, int]:
    
    """Función para generar el sinesweep dada una frecuencia mínima y máxima, una duración T en segundos,
    una frecuencia de sampleo, amplitud de la señal y cantidad de repeticiones para realizar el promedio.
    
    Datos del sinesweep:
    
    f_inf: Frecuencia de inicio en Hz
    f_sup: Frecuencia de finalización en Hz
    T: Duración en segundos
    Fs: Frecuencia de sampleo
    A: Amplitud (valor de 0 a 1)
    P: Repetición, siempre mayor o igual a 1
    """

    t = np.linspace(0, T, Fs*T)

    w1 = 2*np.pi*f_inf
    w2 = 2*np.pi*f_sup
    K = (T*w1)/(np.log(w2/w1))
    L = T/(np.log(w2/w1))

    theta = np.array([K*(np.exp(t[i]/L)-1) for i in range(len(t))])
    x_t = np.array([np.sin(theta[i]) for i in range(len(t))]) # sinesweep

    x_tp = []
    for _ in range(P):
        for i in range(len(x_t)):
            x_tp.append(x_t[i])  # concateno los sweeps

    norm = np.max(np.abs(x_tp))
    x_tNorm = np.zeros(len(x_tp))

    for i in range(len(x_tp)):
        x_tNorm[i] = x_tp[i]/norm  # sinesweep normalizado

    x_tNorm = np.multiply(x_tNorm, A)  # Determino su amplitud

    # Modulacion
    w_t = (K/L)*np.exp(t/L)
    m_t = np.multiply(1/(2*np.pi*w_t), w1)

    m_tp = []
    for p in range(P):
        for i in range(len(m_t)):
            m_tp.append(m_t[i])  # concateno los sweeps

    # Filtro Inverso
    x_t2 = np.flip(x_tp)
    k_t = np.multiply(m_tp, x_t2)  # Filtro inverso

    k_tNorm = np.zeros(len(k_t))
    norm = np.max(np.abs(k_t))

    for i in range(len(k_t)):
        k_tNorm[i] = k_t[i]/norm  # Filtro inverso normalizado

    k_tNorm = np.multiply(k_tNorm, A)  # Determino su amplitud

    print(f"Se creó un sinesweep de {f_inf} a {f_sup} Hz, de {T} segundos de duración, amplitud {A} y promedio {P}")

    return x_tNorm, k_tNorm, T, Fs, P

def get_ir(sinesweep_data: np.ndarray, filtro_inverso: np.ndarray, Fs: int, P: int) -> np.ndarray:
    
    samples = int(T*Fs)
    #aux = np.zeros(int(len(sinesweep_data[0:samples])))
    aux = np.zeros(int(2*len(sinesweep_data[0:samples])-1))

    for i in range(P):
        #fft del lado derecho:
        #filtro_inverso_f = rfft(filtro_inverso[int(samples*i):int(samples*(i+1))])
        #f = rfft(sinesweep_data[int(samples*i):int(samples*(i+1))])

        #Convoluciono señal con filtro inverso para obtener la IR en frecuencia:
        #f = np.array(f)*np.array(filtro_inverso_f)

        #Paso a muestras:
        #signal = irfft(f)

        signal = fftconvolve(filtro_inverso[int(samples*i):int(samples*(i+1))], 
                             sinesweep_data[int(samples*i):int(samples*(i+1))])

        #Sumo todas para luego hacer el promedio:
        aux = signal + aux
    
    #Saco el promedio de las mediciones:
    IR = aux / P

    IR = IR/np.max(np.abs(IR)) #Normalizo

    #idx = int(np.where(abs(IR) == np.max(abs(IR)))[0])#Agarro desde el máximo

    #IR = IR[idx:]

    return IR



if __name__ == '__main__':

    #Datos del sinesweep
    f_inf: int = 20    #Frecuencia inferior
    f_sup: int = 20000 #Frecuencia superior
    T: int = 5         #Duración en segundos
    Fs: int = 44100    #Frecuencia de sampleo
    A: float = 1.0     #Amplitud
    P: int = 1         #Cantidad de repeticiones

    #Grabo el sinesweep:
    sinesweep_data, filtro_inverso, T, Fs, P = sinesweep(f_inf, f_sup, T, Fs, A, P)
    myrecording = sd.playrec(sinesweep_data, Fs, channels=1)
    sd.wait()

    myrecording = myrecording.flatten()

    #Obtengo la IR:
    IR = get_ir(myrecording, filtro_inverso, Fs, P)

    #Guardo el audio:
    sf.write('IR.wav', IR, Fs)
