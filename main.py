import code.audio_tests as audio_tests
import customtkinter
from tkinter import *
from code.informe import informe
from code.test_warble_tone.warble_tone import FcError

def calibracion() -> None:
    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    #Genero la calibración:
    tests.record_calibration()

def linealidad_aerea() -> None:

    global result_linealidad_aerea

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    result_linealidad_aerea = tests.get_linealidad_aerea()

def linealidad_osea() -> None:

    global result_linealidad_osea

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    result_linealidad_osea = tests.get_linealidad_osea()

def tono_pulsante() -> None:

    global reslut_tono_pulsante

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    reslut_tono_pulsante = tests.get_pulse_tone()

def warble_tone() -> None:

    global result_warble_tone

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    result_warble_tone = tests.get_warble_tone()

def nivel_vocal() -> None:

    global result_nivel_vocal

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    result_nivel_vocal = tests.get_nivel_vocal()

def ruido() -> None:

    global result_ruido

    #Especifico el auricular a utilizar:
    auricular = tipo_auricular.get()
    tests.set_auricular(auricular)

    result_ruido = tests.get_ruido()

def gen_informe() -> None:

    #result_linealidad_aerea = None
    #result_linealidad_osea = None
    #reslut_tono_pulsante = None
    #result_warble_tone = None
    #result_nivel_vocal = None
    #result_ruido = None
    
    informe.gen_informe(result_linealidad_aerea,
                        result_linealidad_osea,
                        reslut_tono_pulsante,
                        result_warble_tone,
                        result_nivel_vocal,
                        result_ruido)
                        
    print('Informe generado!')

if __name__ == '__main__':

    #Instancio la clase con los tests:
    sr = 44100
    tests = audio_tests.Tests(sr)

    global root

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = customtkinter.CTk()
    root.title("Informe de pruebas de audio")
    root.geometry("330x560")
    root.iconbitmap('logo.ico')

    recomendacion0 = customtkinter.CTkLabel(root, text='Seleccione el tipo de auricular:')
    recomendacion0.grid(row=0, column=0, pady=5, padx=50)
    tipo_auricular = customtkinter.CTkOptionMenu(root, values=["Supraural (ej: JBL600)", "Circumaural (ej: JBL750)", "Vincha osea"])
    tipo_auricular.grid(row=2, column=0, pady=5, padx=50)
    tipo_auricular.set("Supraural (ej: JBL600)")

    recomendacion1 = customtkinter.CTkLabel(root, text='Calibrar cada vez que mueva la ganancia')
    recomendacion1.grid(row=4, column=0, pady=5, padx=50)

    cal_low = customtkinter.CTkButton(root, text="Calibración", command=calibracion)
    cal_low.grid(row=5, column=0, pady=5, padx=50)

    recomendacion1 = customtkinter.CTkLabel(root, text='Pruebas:')
    recomendacion1.grid(row=6, column=0, pady=5, padx=50)

    record_linelidad_osea = customtkinter.CTkButton(root, text="Linealidad ósea", command=linealidad_osea)
    record_linelidad_osea.grid(row=7, column=0, pady=5, padx=50)

    record_linelidad_aerea = customtkinter.CTkButton(root, text="Linealidad aérea", command=linealidad_aerea)
    record_linelidad_aerea.grid(row=8, column=0, pady=5, padx=50)

    record_tono_pulsante = customtkinter.CTkButton(root, text="Tono pulsante", command=tono_pulsante)
    record_tono_pulsante.grid(row=9, column=0, pady=5, padx=50)

    record_warble_tone = customtkinter.CTkButton(root, text="Warble tone", command=warble_tone)
    record_warble_tone.grid(row=10, column=0, pady=5, padx=50)

    record_nivel_vocal = customtkinter.CTkButton(root, text="Nivel vocal", command=nivel_vocal)
    record_nivel_vocal.grid(row=11, column=0, pady=5, padx=50)

    record_ruido = customtkinter.CTkButton(root, text="Ruido", command=ruido)
    record_ruido.grid(row=12, column=0, pady=5, padx=50)

    global progress_label
    progress_label = StringVar()
    progress_label.set("")
    recomendacion2 = customtkinter.CTkLabel(root, textvariable=progress_label)
    recomendacion2.grid(row=13, column=0, pady=5, padx=50)

    progress = customtkinter.CTkProgressBar(root)
    progress.grid(row=14, column=0, pady=5, padx=50)
    progress.set(0)

    calculate = customtkinter.CTkButton(root, text="Informe", command=gen_informe)
    calculate.grid(row=15, column=0, pady=5, padx=50)

    root.mainloop()