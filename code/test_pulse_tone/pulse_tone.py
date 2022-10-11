import sys
# Agrego el path donde está el tone_generator al archivo:
sys.path.append('../')
import tone_generator
""" Configuración:
Tipos de tonos:
tone_generator.AUDIOMETRY_TONE
tone_generator.REPEATED_TONE       
tone_generator.DEMO_TONE           
tone_generator.USER_REPEATED_TONE  
tone_generator.CONTINUOUS_TONE     
tone_generator.PULSE_TONE_HALF_SEC 
tone_generator.PULSE_TONE_ONE_SEC  
tone_generator.MASKING_STIMULUS    
tone_generator.WARBLE_TONE         
tone_generator.LINEARITY_TEST

Seteo de valores: 
pToneGen->bypass: 0x0
pToneGen->freq: 0x1
pToneGen->gain: 0x2
pToneGen->pan: 0x3 
pToneGen->interval: 0x4 
pToneGen->initGain: 0x5
pToneGen->finalGain: 0x6
pToneGen->gainChange: 0x7 
pToneGen->gainThreshold: 0x8 
pToneGen->toneType: 0x9
pToneGen->pulseSamples: 0xA 
pToneGen->intercomVolume: 0xB 
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

def tone(sr, frec, tone_type, gain, chanel, buffer):

    tone_generator.tone_generator_free()

    tone_generator.tone_generator_alloc(sr)
    tone_generator.tone_generator_setValue(0x0, 0) #Saco el bypass!
    tone_generator.tone_generator_setValue(0x1, frec) #Frecuencia en [Hz]
    tone_generator.tone_generator_setValue(0x9, tone_type) #Tipo de tono
    tone_generator.tone_generator_setValue(0x2, gain) #Ganancia en dBFS
    tone_generator.tone_generator_setValue(0x3, chanel) #Canal de emisión

    data = tone_generator.tone_generator_interval_process(buffer)
    data = data.tolist()

    # Me quedo solo con el canal elegido y elimino los 0:
    tono = []
    if chanel == 0x4: #Canal izquierdo
        for i in range(0, len(data), 2):
            tono.append(data[i])
    elif chanel == 0x5: #Canal derecho
        for i in range(1, len(data), 2):
            tono.append(data[i])

    tone_generator.tone_generator_free()

    plt.plot(tono)
    plt.show()

    tono = np.abs(hilbert(tono))

    plt.plot(tono)
    plt.show()

    return tono

# Defino los parámetros:
sr = 48000 # Frecuencia de sampleo [Hz]
frec = 1000 # Frecuencia [Hz]
tone_type = tone_generator.PULSE_TONE_HALF_SEC # Tipo de tono
gain = 0 # Ganancia en dBFs
chanel = 0x4 # Canal izquierdo = 0x4, Canal derecho = 0x5
audio_seconds = 2 #Segundos de audio que quiero
buffer = int(sr*audio_seconds*2) #(frecuencia de sampleo)*(segundos de audio)*(canales)

#Genero el test:
tono = tone(sr, frec, tone_type, gain, chanel, buffer)



tono = tono[int(0.35*sr):int(1.75*sr)]

#df = pd.DataFrame({'Tono' : tono})
#df.to_csv('Tono pulsante.csv', index=False)

time = np.linspace(0.35, 1.75, num=int(sr*(1.75-0.35)))

min = np.min(np.abs(tono))
max = np.max(np.abs(tono))

print(np.where(tono>=max*0.1))

rise_init = np.where(tono>=max*0.1)[0][0]
rise_end = np.where(tono>=max*0.9)[0][0]

#print(time[rise_init])
#print(time[rise_end])

tono2 = tono[rise_end+10:-1]

fall_init = np.where(tono2<=max*0.9)[0][0]
fall_end = np.where(tono2<=max*0.1)[0][0]
middle_1 = np.where(tono2<=max*0.5)[0][0]

tono3 = tono[fall_end+10+rise_end+10:-1]

middle_2 = np.where(tono3>=max*0.5)[0][0]

#print(fall_init)
#print(fall_end)

print(f'Rise time: {(time[rise_end]-time[rise_init])*10**3} ms')
print(f'Fall time: {(time[fall_end]-time[fall_init])*10**3} ms')
print(f'On time: {(time[fall_init+rise_end+10]-time[rise_end])*10**3} ms')
print(f'Middle/Fall time: {(time[fall_end+rise_end+10]-time[middle_1+rise_end+10])*10**3} ms')
print(f'On/Off time: {(time[middle_2+fall_end+10+rise_end+10]-time[middle_1+rise_end+10])*10**3} ms')


plt.plot(time, np.abs(tono))

font = {'color':  'black',
        'weight': 'normal',
        'size': 8,
        }

plt.axvline(x = 0.35+rise_init/sr, color = 'r')
plt.axvline(x = 0.35+rise_end/sr, color = 'r')
plt.axvline(x = 0.35+(fall_init+rise_end+10)/sr, color = 'r')
plt.axvline(x = 0.35+(fall_end+rise_end+10)/sr, color = 'r')
plt.axvline(x = 0.35+(middle_2+fall_end+10+rise_end+10)/sr, color = 'y')
plt.axvline(x = 0.35+(middle_1+rise_end+10)/sr, color = 'g')
plt.text(1.6, 0.75, f"""Rise time: {np.round((time[rise_end]-time[rise_init])*10**3,1)} ms\n
Fall time: {np.round((time[fall_end]-time[fall_init])*10**3,1)} ms\n
On time: {np.round((time[fall_init+rise_end+10]-time[rise_end])*10**3,1)} ms\n
On/Off time: {np.round((time[middle_2+fall_end+10+rise_end+10]-time[middle_1+rise_end+10])*10**3,1)} ms""",
        fontdict=font, ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.show()