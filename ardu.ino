void toArduinoScopio(int canal1, int canal2) 
{
	Serial.print("ArduinoScopio:");
	Serial.print(canal1);
	Serial.print(" ");
	Serial.println(canal2);
}

void setup()
{
	Serial.begin(9600);
}

void loop()
{
	toArduinoScopio(0, analogRead(A0));
	delay(200);
}