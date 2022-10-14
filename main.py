import code.test_linealidad.linelidad as linealidad
#from code.test_nivel_vocal.nivel_vocal import 
import code.test_pulse_tone.pulse_tone as pulse_tone
#from code.test_respuesta_en_frecuencia.rta_frec import
#from code.test_ruido.ruido import
#from code.informe.informe import
from code.record_audio import *

import customtkinter
from tkinter import *

def calcular():
    pass

def record_cal():
    pass

def record_data():
    pass

if __name__ == '__main__':

    linealidad.linealidad2()
    linealidad.linealidad3()

    pulse_tone.test()

    global root

    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = customtkinter.CTk()
    root.title("Informe de pruebas de audio")
    root.geometry("330x580")
    root.iconbitmap('logo.ico')

    recomendacion0 = customtkinter.CTkLabel(root, text='Seleccione el tipo de auricular:')
    recomendacion0.grid(row=0, column=0, pady=5, padx=50)
    tipo_auricular = customtkinter.CTkOptionMenu(root, values=["Supraural (ej: JBL600)", "Circumaural (ej: JBL750)"])
    tipo_auricular.grid(row=2, column=0, pady=5, padx=50)
    tipo_auricular.set("Supraural (ej: JBL600)")

    recomendacion1 = customtkinter.CTkLabel(root, text='Calibrar cada vez que mueva la ganancia')
    recomendacion1.grid(row=4, column=0, pady=5, padx=50)

    cal_low = customtkinter.CTkButton(root, text="Calibración", command=record_cal)
    cal_low.grid(row=5, column=0, pady=5, padx=50)

    recomendacion1 = customtkinter.CTkLabel(root, text='')
    recomendacion1.grid(row=6, column=0, pady=5, padx=50)

    record_linelidad_aerea = customtkinter.CTkButton(root, text="Linealidad aérea", command=record_data)
    record_linelidad_aerea.grid(row=7, column=0, pady=5, padx=50)

    record_linelidad_osea = customtkinter.CTkButton(root, text="Linealidad ósea", command=record_data)
    record_linelidad_osea.grid(row=8, column=0, pady=5, padx=50)

    record_tono_pulsante = customtkinter.CTkButton(root, text="Tono pulsante", command=record_data)
    record_tono_pulsante.grid(row=9, column=0, pady=5, padx=50)

    record_nivel_vocal = customtkinter.CTkButton(root, text="Nivel vocal", command=record_data)
    record_nivel_vocal.grid(row=10, column=0, pady=5, padx=50)

    record_ruido = customtkinter.CTkButton(root, text="Ruido", command=record_data)
    record_ruido.grid(row=11, column=0, pady=5, padx=50)

    global progress_label
    progress_label = StringVar()
    progress_label.set("")
    recomendacion2 = customtkinter.CTkLabel(root, textvariable=progress_label)
    recomendacion2.grid(row=12, column=0, pady=5, padx=50)

    progress = customtkinter.CTkProgressBar(root)
    progress.grid(row=13, column=0, pady=5, padx=50)
    progress.set(0)

    file_name_recomendacion = customtkinter.CTkLabel(root, text='Nombre del informe:')
    file_name_recomendacion.grid(row=14, column=0, pady=5, padx=50)

    file_name_entry = customtkinter.CTkEntry(root, justify=LEFT, textvariable='Nombre del informe')
    file_name_entry.grid(row=15, column=0, pady=5, padx=50)

    calculate = customtkinter.CTkButton(root, text="Calcular", command=calcular)
    calculate.grid(row=16, column=0, pady=5, padx=50)

    root.mainloop()