
# **Projeto de Detecção de Sono em Motoristas com Visão Computacional**

Este projeto visa criar um sistema de detecção de sono em motoristas utilizando **visão computacional** para monitorar os olhos do motorista e **Arduino virtual** para indicar um alarme, alertando o motorista quando ele estiver com os olhos fechados por um longo período. O objetivo principal é evitar acidentes em empresas de fretados, alertando motoristas que podem estar dormindo ao volante.

## **Tecnologias Utilizadas**

- **Python**: Linguagem principal para implementar a lógica de detecção de olhos fechados utilizando **OpenCV**.
- **OpenCV**: Biblioteca de visão computacional utilizada para capturar e processar a imagem da câmera em tempo real.
- **SimulIDE**: Simulador de Arduino para simular o funcionamento do sistema sem hardware físico.
- **COM0COM**: Ferramenta de emulação de portas seriais para permitir a comunicação entre o código Python e o SimulIDE via comunicação serial.
- **Arduino IDE**: Utilizado para carregar o código no Arduino (usado para a simulação no SimulIDE).

## **Objetivo do Projeto**

Este sistema tem como objetivo:
1. Monitorar o motorista em tempo real para verificar se ele está com os olhos fechados.
2. Quando os olhos do motorista ficarem fechados por mais de **2 segundos**, um alarme será acionado.
3. O alarme é representado por **LEDs** (vermelho para alerta e verde para acordado).
4. A comunicação entre o Python e o Arduino virtual será feita por **COM0COM**, utilizando duas portas seriais virtuais.

## **Estrutura do Projeto**

1. **SimulIDE**:
   - Contém o **Arduino virtual** com **LEDs** conectados aos pinos **13** (LED verde) e **12** (LED vermelho).
   - Utiliza a **porta COM virtual** criada pelo **COM0COM** para se comunicar com o Python.

2. **Python**:
   - Utiliza **OpenCV** para capturar a imagem da câmera e aplicar um modelo Haar Cascade para detectar rostos e olhos.
   - Envia comandos para o Arduino virtual para controlar os LEDs (vermelho para alerta e verde para indicar que o motorista está acordado).

3. **COM0COM**:
   - Cria dois pares de portas seriais virtuais:
     - **COM1** (SimulIDE/Arduino virtual)
     - **COM2** (Python)
   - Permite que o **Python** e o **SimulIDE** se comuniquem sem a necessidade de hardware físico.

## **Como Funciona**

1. O **Python** captura a imagem da câmera em tempo real e usa **OpenCV** para detectar se os olhos do motorista estão fechados.
2. Quando os olhos permanecem fechados por mais de 2 segundos, o **Python** envia o comando `ALERT` para o **SimulIDE**, acionando o **LED vermelho**.
3. Se os olhos do motorista estiverem abertos, o Python envia um comando vazio, acionando o **LED verde**.
4. A comunicação entre o **Python** e o **SimulIDE** acontece por meio da comunicação serial via portas virtuais criadas pelo **COM0COM**.

## **Configuração do Projeto**

### **Pré-requisitos**

- **Python 3.x**
- **OpenCV**: Para instalar, execute:
  ```bash
  pip install opencv-python
  ```
- **COM0COM**: Para criar as portas seriais virtuais.
  - Baixe e instale no [site oficial](https://sourceforge.net/projects/com0com/).
- **SimulIDE**: Para simular o Arduino.
  - Baixe e instale no [site oficial](https://www.simulide.com/).
- **Arduino IDE**: Para programar o Arduino (usado para a simulação no SimulIDE).

### **Configuração do COM0COM**

1. Abra o **COM0COM Setup** e crie um par de portas seriais:
   - **COM1**: Usada pelo **SimulIDE**.
   - **COM2**: Usada pelo **Python**.

2. Configure a **porta COM1** no **SimulIDE** e a **porta COM2** no **Python**.

### **Configurando o SimulIDE**

1. Abra o **SimulIDE** e adicione o **Arduino virtual**.
2. Conecte os **LEDs** aos pinos 13 (verde) e 12 (vermelho) do Arduino virtual.
3. Configure a **porta COM1** para comunicação serial com o **Python**.

### **Código Python**

1. O código Python usa **OpenCV** para capturar a imagem da câmera e verificar se os olhos estão fechados.
2. **Exemplo de código Python**:

```python
import serial
import time

# Configuração da comunicação serial com a porta COM2
ser = serial.Serial('COM2', 9600)

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
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if check_eyes_closed(eyes):
            time_eyes_closed += 1
        else:
            time_eyes_closed = 0

        if time_eyes_closed >= eyes_closed_threshold:
            ser.write(b'ALERT
')  # Envia o alerta para o Arduino no SimulIDE
        else:
            ser.write(b'
')  # Reseta o alerta

    cv2.imshow('Detectando Olhos Fechados', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### **Código do Arduino no SimulIDE**

1. O código no **SimulIDE** controla os LEDs com base nos comandos recebidos pela comunicação serial.

```cpp
const int ledVerdePin = 13;  // LED verde no pino 13
const int ledVermelhoPin = 12;  // LED vermelho no pino 12

void setup() {
  pinMode(ledVerdePin, OUTPUT);
  pinMode(ledVermelhoPin, OUTPUT);
  Serial.begin(9600);  // Comunicação serial com o Python
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();  // Lê o comando enviado pelo Python
    
    if (command == "ALERT") {
      digitalWrite(ledVermelhoPin, HIGH);  // Acende o LED vermelho
      digitalWrite(ledVerdePin, LOW);  // Apaga o LED verde
    } else {
      digitalWrite(ledVermelhoPin, LOW);  // Apaga o LED vermelho
      digitalWrite(ledVerdePin, HIGH);  // Acende o LED verde
    }
  }
}
```

## **Conclusão**

Este projeto usa **visão computacional** para detectar quando um motorista está com os olhos fechados por mais de 2 segundos e ativa um alarme visual (LED vermelho) utilizando **SimulIDE** e **Arduino virtual**. A comunicação entre o **Python** e o **SimulIDE** ocorre via **COM0COM**, criando portas seriais virtuais para garantir que o **SimulIDE** e o **Python** possam se comunicar sem conflitos.


