const int echoPin1 = 8;
const int trigPin1 = 9;

long duration = 0;
int distance = 0;

void setup(){
  Serial.begin(115200);

  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);
}

void loop(){
  distance = getDistance(trigPin1, echoPin1);
  if (distance != -1) {
    Serial.println("Distance: " + String(distance));
  }
}

int getDistance(int trigPin, int echoPin)
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  duration = duration * 0.034 / 2;
  if (duration > 100) {
    return -1;
  }
  else {
    return duration;
  }
}