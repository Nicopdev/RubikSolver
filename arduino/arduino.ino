char s_start = '!';
char s_end = ';';

char up = 'U';
char down = 'D';
char left = 'L';
char right = 'R';
char front = 'F';
char back = 'B';
char two_times = '2';
char three_times = '3';

char datafromUser;

void setup() {
  // put your setup code here, to run once:
  pinMode( LED_BUILTIN , OUTPUT );

  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  
  Serial.begin(9600);
  delay(1000);
  Serial.print(s_start);
  delay(100);
}

String solve = "";
String lastSolve = "";
bool full_msg = false;
void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    datafromUser = Serial.read();
    Serial.flush();

    if (datafromUser == s_start) {
      full_msg = false;
      solve = "";
    } else if (datafromUser == s_end) {
      full_msg = true;
    } else {
      solve += datafromUser;
    }

    if (full_msg) {
      lastSolve = solve;
      Serial.println(lastSolve);
    }
    
    if (datafromUser != s_start) {
      // SWITCH
    }
        
   }
}
