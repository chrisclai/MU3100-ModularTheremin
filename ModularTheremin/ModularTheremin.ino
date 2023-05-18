const int trigPin1 = 15;
const int echoPin1 = 14;
const int trigPin2 = 2;
const int echoPin2 = 3;
const int trigPin3 = 4;
const int echoPin3 = 5;

const int trigPin4 = 6;
const int echoPin4 = 7;
const int trigPin5 = 8;
const int echoPin5 = 9;
const int trigPin6 = 10;
const int echoPin6 = 11;


long duration = 0;
int distance = 0;
int distance1 = 0;
int distance2 = 0;
int distance3 = 0;
int distance4 = 0;
int distance5 = 0;
int distance6 = 0;

int leftnote = 0;
int rightnote = 0;

void setup(){
  Serial.begin(115200);

  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin3, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin4, INPUT);
  pinMode(trigPin4, OUTPUT);
  pinMode(echoPin5, INPUT);
  pinMode(trigPin5, OUTPUT);
  pinMode(echoPin6, INPUT);
  pinMode(trigPin6, OUTPUT);
}

void loop(){
  // Get all distances
  // distance1 = getDistance(trigPin1, echoPin1);
  distance2 = getDistance(trigPin2, echoPin2);
  // distance3 = getDistance(trigPin3, echoPin3);
  // distance4 = getDistance(trigPin4, echoPin4);
  distance5 = getDistance(trigPin5, echoPin5);
  // distance6 = getDistance(trigPin6, echoPin6);

  Serial.println(String(distance2) + " " + String(distance5));
  // Serial.println(String(distance1) + " " + String(distance3) + " " + String(distance4) + " " + String(distance6));
}

int getDistance(int trigPin, int echoPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  if (distance > 48) {
    return -1;
  }
  else {
    return distance / 4;
  }
}