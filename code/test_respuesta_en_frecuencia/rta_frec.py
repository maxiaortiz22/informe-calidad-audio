from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
from scipy.fft import rfft, rfftfreq
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def sinesweep(f_inf: int = 20, 
              f_sup: int = 20000, 
              T: int = 5, 
              Fs: int = 44100, 
              A: float = 1.0, 
              P: int = 1) -> tuple[np.ndarray, np.ndarray, int, int, int]:
    
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


def rta(sinesweep_data: np.ndarray, 
        filtro_inverso: np.ndarray, 
        T: int, 
        Fs: int, 
        P: int) -> tuple[np.ndarray, np.ndarray]:

    """Función para emitir y grabar un sinesweep, con los sinesweep de entrada, sus filtros inversos,
    tiempo de duración de cada uno, frecuencia de sampleo y cantidad de sinesweeps para realizar el
    promedio."""

    #Reproduzco y grabo el sinesweep:
    print('Iniciando Sinesweep')
    sinesweep_play = np.zeros((len(sinesweep_data), 2))

    for i in range(len(sinesweep_data)):
        sinesweep_play[i, 0] = sinesweep_data[i]
        sinesweep_play[i, 1] = sinesweep_data[i]

    #print(sinesweep_play)
    myrecording = sd.playrec(sinesweep_data, Fs, channels=2)
    sd.wait()

    #sf.write('recording.wav', myrecording, Fs)

    #Separo entre canal izquierdo y derecho:
    left = np.zeros(len(myrecording[:, 0]))
    right = np.zeros(len(myrecording[:, 1]))

    for i in range(len(myrecording[:, 0])):
        left[i] = myrecording[i, 0]
        right[i] = myrecording[i, 1]

    #Obtengo la transformada de Fourier para cada uno y hago el promedio:
    samples = int(T*Fs)
    left_aux = np.zeros(int(2*len(left[0:samples])-1))
    right_aux = np.zeros(int(2*len(right[0:samples])-1))

    for i in range(P):
        #fft del lado derecho:
        #filtro_inverso_f = rfft(filtro_inverso[int(samples*i):int(samples*(i+1))])
        #left_f = rfft(left[int(samples*i):int(samples*(i+1))])
        #right_f = rfft(right[int(samples*i):int(samples*(i+1))])

        #Convoluciono señal con filtro inverso para obtener la IR en frecuencia:
        #left_f = np.abs(np.array(left_f)*np.array(filtro_inverso_f))
        #right_f = np.abs(np.array(right_f)*np.array(filtro_inverso_f))

        #Paso a dB:
        #left_F = 20*np.log10(abs(left_f) / (20*np.power(10, 1/6)))
        #right_F = 20*np.log10(abs(right_f) / (20*np.power(10, 1/6)))

        #Sumo todas para luego hacer el promedio:
        #left_f_aux = left_f_aux + left_F
        #right_f_aux = right_f_aux + right_F

        cut_left = fftconvolve(filtro_inverso[int(samples*i):int(samples*(i+1))], 
                               left[int(samples*i):int(samples*(i+1))])

        cut_right = fftconvolve(filtro_inverso[int(samples*i):int(samples*(i+1))], 
                                right[int(samples*i):int(samples*(i+1))])

        #Sumo todas para luego hacer el promedio:
        left_aux = left_aux + cut_left
        right_aux = right_aux + cut_right
    
    #Saco el promedio de las mediciones:
    left_IR = left_aux / P
    right_IR = right_aux / P

    i_left = int(np.where(abs(left_IR) == np.max(abs(left_IR)))[0])
    i_right = int(np.where(abs(right_IR) == np.max(abs(right_IR)))[0])

    left_IR = left_IR[i_left:]
    right_IR = right_IR[i_right:]

    sf.write('rir_left.wav', left_IR, Fs)
    sf.write('rir_right.wav', right_IR, Fs)

    #Paso a dB:
    #left_IR = 20*np.log10(abs(left_IR) / (20*np.power(10, 1/6)))
    #right_IR = 20*np.log10(abs(right_IR) / (20*np.power(10, 1/6)))

    #Vector de frecuencias:
    #N = int(T*Fs)
    #xf = rfftfreq(N, 1 / Fs)

    print('Fin Sinesweep')

    return left_IR, right_IR #, xf

def get_rta_frec(f_inf: int = 20, 
                 f_sup: int = 20000, 
                 T: int = 5, 
                 Fs: int = 44100, 
                 A: float = 1.0, 
                 P: int = 1) -> None:

    #https://stackoverflow.com/questions/43925337/matplotlib-returning-a-plot-object

    #Grabo y obtengo la data:
    sinesweep_data, filtro_inverso, T, Fs, P = sinesweep(f_inf, f_sup, T, Fs, A, P)
    left_IR, right_IR = rta(sinesweep_data, filtro_inverso, T, Fs, P)

    left_F = np.abs(np.array(rfft(left_IR)))
    right_F = np.abs(np.array(rfft(right_IR)))

    left_F = 20*np.log10(abs(left_F) / (20*np.power(10, 1/6)))
    right_F = 20*np.log10(abs(right_F) / (20*np.power(10, 1/6)))

    N_left = int(left_IR.size)
    N_right = int(right_IR.size)
    
    f_left = rfftfreq(N_left, 1 / Fs)
    f_right = rfftfreq(N_right, 1 / Fs)

    #Normalizo en 1000 Hz:
    idx_left = np.where(f_left>=1000)[0][0]
    idx_right = np.where(f_right>=1000)[0][0]
    left_F = left_F - left_F[idx_left]
    right_F = right_F - right_F[idx_right]

    #Grafico la data:
    
    #Ploteo:
    ftick = [20, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
    labels = ['20', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k', '20k']
    
    fig, axes = plt.subplots(2, 1)

    axes[0].plot(f_left, left_F, label='Izquierdo', color='b')
    axes[0].set_xlabel('Frecuencia [Hz]', fontsize=12, color='black')
    axes[0].set_xscale('log')
    for axis in [axes[0].xaxis]:
        axis.set_major_formatter(ScalarFormatter())
    axes[0].set_ylabel('Izquierdo [dB]', fontsize=12, color='black')
    axes[0].set_xlim(20, 20000)
    axes[0].set_xticks(ftick)
    axes[0].set_xticklabels(labels, rotation=90)
    axes[0].legend()
    axes[0].grid(True, which="both", ls="-")

    axes[1].plot(f_right, right_F, label='Derecho', color='r')
    axes[1].set_xlabel('Frecuencia [Hz]', fontsize=12, color='black')
    axes[1].set_xscale('log')
    for axis in [axes[1].xaxis]:
        axis.set_major_formatter(ScalarFormatter())
    axes[1].set_ylabel('Derecho [dB]', fontsize=12, color='black')
    axes[1].set_xlim(20, 20000)
    axes[1].set_xticks(ftick)
    axes[1].set_xticklabels(labels, rotation=90)
    axes[1].legend()
    axes[1].grid(True, which="both", ls="-")

    plt.tight_layout()
    plt.show()
    plt.savefig('results/test_images/rta_frec.png')