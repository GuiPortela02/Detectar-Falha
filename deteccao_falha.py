import cv2, PySimpleGUI as sg
import numpy as np
from plyer import notification

### Projeto da matéria de Ambiência


CIRCLE = '⚫'
CIRCLE_OUTLINE = '⚪'
def LED(color, key):
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)


# Janelas/Widgets da inteface gráfica
window = sg.Window('MONITOR - ESTEIRA DE OVOS', [[sg.Image(key='-I-'), sg.Image(key='-TH-') ],
                                                [sg.Text('ESTEIRA FUNCIONANDO  '), LED('Green', '-LED0-') ],
                                                [sg.Text('MUITOS OVOS DETECTADOS  '), LED('blue', '-LED1-')],
                                                [sg.Text('OVOS NÃO DETECTADOS  '), LED('red', '-LED2-')],
                                                [sg.Button('Exit')]], location=(800, 400))

#Inputs
video = cv2.VideoCapture("simulando_esteira_ovos.mp4")
cap = cv2.VideoCapture("simulando_esteira_ovos.mp4")
sem_ou_com_ovos = [] # Armazena as informações de "Sem ovos" e "Com ovos"
lista_ovos = []
contador = 0

#Evento - Interface gráfica + Detecção dos ovos
while True:  # The PSG "Event Loop"
    event, values = window.read(timeout=30)  
    if event == sg.WIN_CLOSED or event == 'Exit':  break 
      
    # OVOS
    ret,img = video.read()
    img = cv2.resize(img,(480,840),)
    imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    x,y,w,h = 10,100,450,500
    #imgTh = cv2.adaptiveThreshold(imgGray, 244, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    imgTh = cv2.adaptiveThreshold(imgGray, 244, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 16)
    kernel = np.ones((8,8), np.uint8)
    imgDil = cv2.dilate(imgTh,kernel,iterations=2)
    recorte = imgDil[y:y+h,x:x+w]
    brancos = cv2.countNonZero(recorte)

    cv2.rectangle(imgTh, (x, y), (x + w, y + h), (255, 255, 255), 6)
    cv2.imshow('THRESHOLD', cv2.resize(imgTh,(600,500)))
    


    muitos_ovos = bool
    esteira_sem_ovos = bool
    esteira_ligada = True
    
    # Processando as informações - por ms
    if brancos <= 7000:
        sem_ou_com_ovos.append("Sem ovos")
    else:
        sem_ou_com_ovos.append("Com ovos")

    # Contando as quantidades de "Sem ovos" e "Com ovos"
    qtd_sem_ovos = sem_ou_com_ovos.count("Sem ovos")
    qtd_com_ovos = sem_ou_com_ovos.count("Com ovos")

    if qtd_sem_ovos >= 150:
        notification.notify(title="ESTEIRA", 
                            message= "Esteira sem passagem de ovos por 5 segundos - VERIFICAR",  
                            app_icon = "aviso.ico", 
                            timeout = 20,
                            app_name = "MONITOR")
        sem_ou_com_ovos = []
    elif len(sem_ou_com_ovos) >= 300:
        sem_ou_com_ovos = []


    if qtd_sem_ovos >= 150:
        lista_ovos.append("SEM-OVOS")
    elif qtd_com_ovos  >= 150:
        lista_ovos.append("COM-OVOS")
    elif len(lista_ovos) > 3:
        lista_ovos = []
    

    if lista_ovos.count("SEM-OVOS") >=2:
        esteira_sem_ovos = True
        esteira_ligada = False
    
    #window['-TH-'].update(data=cv2.imencode('.ppm', video_th.read()[1])[1].tobytes())
    window['-I-'].update(data=cv2.imencode('.ppm', cap.read()[1])[1].tobytes())
    window[f'-LED{0}-'].update(CIRCLE if esteira_ligada == True else CIRCLE_OUTLINE)
    window[f'-LED{1}-'].update(CIRCLE if muitos_ovos == True else CIRCLE_OUTLINE)
    window[f'-LED{2}-'].update(CIRCLE if esteira_sem_ovos == True else CIRCLE_OUTLINE) 


    


