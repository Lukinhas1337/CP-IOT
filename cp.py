import cv2
import numpy as np
import serial
import time

# Configuração da comunicação serial com o COM0COM
ser = serial.Serial('COM2', 9600)  # Ajuste a porta conforme necessário

# Carregar os classificadores em cascata para detectar rosto e olhos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Função para verificar se os olhos estão fechados
def check_eyes_closed(eyes):
    if len(eyes) == 0:
        return True
    return False

# Inicializar a captura de vídeo
cap = cv2.VideoCapture(0)

# Variável para monitorar o tempo dos olhos fechados
time_eyes_closed = 0
eyes_closed_threshold = 2  # Tempo em segundos para considerar que o motorista está dormindo

while True:
    # Captura o frame da câmera
    ret, frame = cap.read()

    if not ret:
        break

    # Conversão para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta o rosto
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Desenha um retângulo ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Região do rosto para procurar os olhos
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # Verifica se os olhos estão fechados
        if check_eyes_closed(eyes):
            time_eyes_closed += 1
        else:
            time_eyes_closed = 0

        # Acionar alarme se o tempo dos olhos fechados passar do limiar
        if time_eyes_closed >= eyes_closed_threshold:
            print("Alerta! Motorista possivelmente dormindo.")
            ser.write(b'ALERT\n')  # Envia um sinal para o COM0COM

    # Exibe a imagem com o rosto detectado
    cv2.imshow('Detectando Olhos Fechados', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
