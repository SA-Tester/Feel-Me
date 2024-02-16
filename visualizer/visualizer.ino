// LED PINS
const int L1 = 2;
const int L2 = 3;
const int L3 = 4;
const int L4 = 5;
const int L5 = 6;

// MICROPHONE OUT - KY-037
int d0 = 7;
int a0 = A0;

// INITIAL THRESHOLDS FOR LEDS
int t1 = 320;
int t2 = 330;
int t3 = 334;
int t4 = 338;
int t5 = 342;

// LAST DIGITAL PIN
int lastPin = 6;
int totLED = 5;

float readAnalog = 0;
int readDigital = 0;

void setup() {
  Serial.begin(9600);

  for(int i=0; i<lastPin; i++){
    pinMode(i, OUTPUT);
  }

  pinMode(a0, INPUT);
  pinMode(d0, INPUT);
}

// Function to turn on a LED
void blink(int led){
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(100);
}

void loop() {
  readAnalog = analogRead(a0);
  readDigital = digitalRead(d0);

  Serial.print("Reading Analog: ");
  Serial.print(readAnalog);
  Serial.print(" ");

  Serial.print("Reading Digital: ");
  Serial.print(readDigital);
  Serial.println();

  if(readAnalog >= t1 && readDigital == 0){
    blink(L1);
    blink(L3);
    blink(L5);
  }
  else if(readAnalog >= t1 && readDigital == 1){
    blink(L2);
    blink(L4);
  }
  else if(readAnalog >= t2 && readDigital == 0){
    blink(L1);
    blink(L2);
    blink(L3);
    blink(L4);
    blink(L5);
  }
  else if(readAnalog >= t2 && readDigital == 1){
    blink(L3);
    blink(L4);
    blink(L5);
  }
  else if(readAnalog >= t3 && readDigital == 0){
    blink(L1);
    blink(L4);
    blink(L5);
  }
  else if(readAnalog >= t3 && readDigital == 1){
    blink(L1);
    blink(L4);
  }
  else if(readAnalog >= t4 && readDigital == 0){
    blink(L2);
    blink(L4);
    blink(L5);
  }
  else if(readAnalog >= t4 && readDigital == 1){
    blink(L1);
    blink(L5);
  }
  else if(readAnalog >= t5 && readDigital == 0){
    blink(L1);
    blink(L2);
    blink(L3);
    blink(L4);
  }
  else if(readAnalog >= t5 && readDigital == 1){
    blink(L2);
    blink(L3);
    blink(L4);
    blink(L5);
  }
}
