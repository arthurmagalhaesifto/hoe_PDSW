// INCLUSÃO DE BIBLIOTECAS
#include <Adafruit_GFX.h>    
#include <Adafruit_TFTLCD.h> 
#include <TouchScreen.h>
#include <Servo.h>

// DEFINIÇÕES DE PINOS
#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
#define LCD_RESET A4

// VARIAVEL DOS SERVOS MOTORES

Servo servo1;
Servo servo2;

// DEFINIÇÕES
#define WHITE          0xFFFF
#define YELLOW         0xFFE0
#define RED            0xF800
#define BLUE           0x001F
#define BLACK          0x0000

#define LIGADO         0x07E0
#define DESLIGADO      0xF800

#define MINPRESSURE 10
#define MAXPRESSURE 1000


/*____CALIBRAR TFT LCD_____*/
#define YP A3
#define XM A2
#define YM 9
#define XP 8

#define TS_LEFT 129
#define TS_RT   924
#define TS_TOP  82
#define TS_BOT  896
/*______FIM DA CALIBRAÇÃO______*/

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300); //300 É A SENSITIVIDADE
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

int X, Y;
long corBot[3] = {DESLIGADO, DESLIGADO, DESLIGADO};

TSPoint waitTouch() {
  TSPoint p;
  do {
    p = ts.getPoint();
    pinMode(XM, OUTPUT);
    pinMode(YP, OUTPUT);
  } while ((p.z < MINPRESSURE ) || (p.z > MAXPRESSURE));
  
  p.x = map(p.x, TS_LEFT, TS_RT, 0, 240);
  p.y = map(p.y, TS_BOT, TS_TOP, 0, 320);
  
  return p;
}

void setup() {
  Serial.begin(9600);
  
  tft.reset();
  tft.begin(0x9341); // CÓDIGO DO DRIVER DO SEU DISPLAY
  tft.setRotation(2);
  tft.fillScreen(WHITE);

  IntroScreen();   // DESENHA A TELA DE INTRO
  draw_Buttons(0); // DESENHA TODOS OS BOTOES
  tft.fillRect(0, 0, 240, 50, DESLIGADO);
  tft.setTextColor(WHITE);
  tft.setTextSize (4);
  tft.setCursor(5, 10);
  tft.println(" XMachine ");

  servo1.attach(13);
  servo2.attach(11);
  servo1.write(0);
  servo2.write(0);
}

void loop() {
  TSPoint p = waitTouch();
  X = p.x; Y = p.y;

  DetectButtons(); // DETECTA OS BOTOES

  delay(300);
}

// IMPLEMENTO DE FUNÇÕES

void DetectButtons() {

  if (X < 200 && X > 40) {

    if (Y > 160 && Y < 240) { // LOGICA PARA O BOTAO 1
      Serial.println ("Button 1");
      if (corBot[0] == DESLIGADO) {
         corBot[0] = LIGADO;
         Serial.println ("Funcionou");
         servo1.write(180);
         delay(3000);
         servo1.write(0);
         corBot[0] = DESLIGADO;
      }
      draw_Buttons(1);
    }


    if (Y > 60 && Y < 140) { // LOGICA PARA O BOTAO 2
      Serial.println ("Button 2");
      if (corBot[1] == DESLIGADO) {
         corBot[1] = LIGADO;
         servo2.write(180);
         delay(3000);
         servo2.write(0);
         corBot[1] = DESLIGADO;
      }
      draw_Buttons(2);
    }

  }

}

void IntroScreen() {
  tft.fillScreen(WHITE);
}

void draw_Buttons(int type) {
  switch (type) {
    case 1:
      tft.fillRect  (40, 80 , 160, 80, corBot[0]);

      tft.setTextColor(WHITE);
      tft.setTextSize (4);
      tft.setCursor(100, 110);
      tft.println("01");
      break;

    case 2:
      tft.fillRect  (40, 200, 160, 80, corBot[1]);

      tft.setTextColor(WHITE);
      tft.setTextSize (4);
      tft.setCursor(100, 230);
      tft.println("02");
      break;

    default:
      tft.fillRect  (40, 80 , 160, 80, corBot[0]);
      tft.fillRect  (40, 200, 160, 80, corBot[1]);

      tft.setTextColor(WHITE);
      tft.setTextSize (4);

      tft.setCursor(100, 110);
      tft.println("01");

      tft.setCursor(100, 230);
      tft.println("02");

  }

}