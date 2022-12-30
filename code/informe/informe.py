from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('code/informe/usound.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Informe de calidad de audio', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')

def gen_informe(result_linealidad_aerea,
                result_linealidad_osea,
                reslut_tono_pulsante,
                result_warble_tone,
                result_nivel_vocal,
                result_ruido,
                result_on_off,
                version_app,
                celular,
                calibracion_usada,
                id_informe):

    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', 'B', 12)
    # open the text file in read mode
    e = datetime.datetime.now()
    pdf.cell(0, 5, f'Informe generado el {e.strftime("%d-%m-%Y %H:%M:%S")} - {id_informe}', 0, 1, 'L')

    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.cell(0, 5, f'Versión de la app analizada: {version_app}', 0, 1, 'L')
    pdf.cell(0, 5, f'Dispositivo movil utilizado: {celular}', 0, 1, 'L')
    pdf.cell(0, 5, f'Calibración utilizada: {calibracion_usada}', 0, 1, 'L')

    pdf.cell(0, 5, '', 0, 1, 'L')

    #Test linealidad aérea:
    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de linealidad aérea:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca encontrar la linealidad del test aéreo de 60 a 20 dBHL en todas sus ' + 
                       'frecuencias a pasos de 5 dBHL.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 17
    w = 17
    h = 7

    columnNameList = list(result_linealidad_aerea.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_linealidad_aerea)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_linealidad_aerea['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_linealidad_aerea['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_linealidad_aerea['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test linealidad ósea:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de linealidad ósea:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca encontrar la linealidad del test óseo de 30 a -10 dBHL, en todas sus ' + 
                       'frecuencias a pasos de 5 dBHL.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 17
    w = 17
    h = 7

    columnNameList = list(result_linealidad_osea.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_linealidad_osea)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_linealidad_osea['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_linealidad_osea['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_linealidad_osea['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test de tono pulsante
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de tono pulsante:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='En este test se busca encontrar los tiempos de Rise time, Fall time, ' + 
                       'On time y On/Off time del tono pulsante.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 25
    w = 25
    h = 7

    columnNameList = list(reslut_tono_pulsante.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(reslut_tono_pulsante)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(reslut_tono_pulsante['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(reslut_tono_pulsante['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(reslut_tono_pulsante['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/pulse_tone.png', x=None, y=None, w=0, h=0, type='', link='')

    #Test de nivel vocal:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de nivel vocal:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='Para este test se grabaran a 85 dBHL el conjunto de palabras sin silencio de las listas:\n\n' + 
                       '    * Dr. Tato adultos\n    * Dr. Tato niños\n    * SRT E IRF (masculino)\n' +
                       '    * SRT E IRF (femenino)\n    * Audicom',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 43
    w = 40
    h = 7

    columnNameList = list(result_nivel_vocal.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_nivel_vocal)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_nivel_vocal['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_nivel_vocal['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_nivel_vocal['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    #Test de encendido/apagado:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de encendido/apagado del tono', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='Para este test se busca encontrar los tiempos de encendido y apagado al reproducir un tono con ' + 
                       'el test de aéreo.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 25
    w = 25
    h = 7

    columnNameList = list(result_on_off.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_on_off)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_on_off['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_on_off['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_on_off['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/on_off_tono.png', x=None, y=None, w=0, h=0, type='', link='')

    #Test de ruido:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de ruido:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='Para este test se graban a 60 dBHL 3 tipos de ruido: Blanco, Vocal y NBN a 1kHz. ' + 
                       'Para su representación, se observa una tabla con los valores obtenidos y la ' +
                       'respuesta en frecuencia de cada uno.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 30
    w = 30
    h = 7

    columnNameList = list(result_ruido.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_ruido)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_ruido['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_ruido['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_ruido['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/Ruido blanco.png', x=None, y=None, w=0, h=0, type='', link='')
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/Ruido vocal.png', x=None, y=None, w=0, h=0, type='', link='')
    pdf.cell(90, 5, ' ', 0, 2, 'C')

    pdf.image('results/test_images/NBN 1kHz.png', x=None, y=None, w=0, h=0, type='', link='')

    #Test de Warble tone:
    pdf.add_page()

    pdf.set_font('Times', 'U', 14)
    pdf.cell(0, 5, f'Test de warble Tone:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 5, '', 0, 1, 'L')

    pdf.multi_cell(w=0, h=5, 
                   txt='Para este test se buscan las frecuencia de mensaje y moduladora del Warble Tone.',
                   border=0, fill=False, align='J')
    pdf.cell(0, 5, '', 0, 1, 'L')

    w_firt_col = 51
    w = 51
    h = 7

    columnNameList = list(result_warble_tone.columns)
    totColumns = len(columnNameList)

    w_len = w_firt_col + w*(totColumns-2)

    i=0
    for header in columnNameList[:-1]:
        if i%totColumns == 0:
            pdf.cell(w_firt_col, h, header, 1, 0, 'C')
            i+=1
        else:
            pdf.cell(w, h, header, 1, 0, 'C')
            i+=1
    pdf.cell(w, h, columnNameList[-1], 1, 2, 'C')
    pdf.cell(-1*(w_len))
    pdf.set_font('arial', '', 11)

    i=0
    for row in range(0, len(result_warble_tone)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList)-1:
                if col_num==0:
                    pdf.cell(w_firt_col,h, str(result_warble_tone['%s' % (col_name)].iloc[row]), 1, 0, 'C')
                else:
                    pdf.cell(w,h, str(result_warble_tone['%s' % (col_name)].iloc[row]), 1, 0, 'C')
            else:
                pdf.cell(w,h, str(result_warble_tone['%s' % (col_name)].iloc[row]), 1, 2, 'C')
                pdf.cell(-1*(w_len))

    pdf.output(name=f'results/Informe de calidad de Audio {id_informe}.pdf')