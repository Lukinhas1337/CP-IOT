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
      // Se o comando for ALERT, acende o LED vermelho e apaga o verde
      digitalWrite(ledVermelhoPin, HIGH);  
      digitalWrite(ledVerdePin, LOW);
    } else {
      // Se o comando for vazio, acende o LED verde e apaga o vermelho
      digitalWrite(ledVermelhoPin, LOW);
      digitalWrite(ledVerdePin, HIGH);
    }
  }
}
