#Programa: Motor de passo 28BYJ-48 e Raspberry Pi 2
#Alteracoes e adaptacoes : Arduino e Cia
#
#Baseado no codigo original de Matt Hawkins
#http://www.raspberrypi-spy.co.uk/

#Carrega bibliotecas
import sys
import time
import RPi.GPIO as GPIO

#Utiliza numeros da GPIO ao inves
#da numeracao dos pinos
GPIO.setmode(GPIO.BCM)

#Pinos de conexao ao motor
#Pinos 40, 38, 36, 32
#GPIO21,GPIO20,GPIO16,GPIO12
StepPins = [21,20,16,12]

#Define os pinos como saida
for pin in StepPins:
  print ("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

#Sequencia de ativacao
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]
       
StepCount = len(Seq)-1

#Configura sentido de giro
StepDir = 2 # 1 ou 2 para sentido horario
            # -1 ou-2 para sentido anti-horario

#Tempo de espera
WaitTime = 3/float(1000)

#Inicializa variaveis
StepCounter = 0

while True:
  #Movimenta o motor e envia os dados de ativacao
  #para o display
  for pin in range(0, 4):
    xpin = StepPins[pin]
    print (StepCounter)
    if Seq[StepCounter][pin]!=0:
      print (" Step %i Enable %i" %(StepCounter,xpin))
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)

  StepCounter += StepDir

  #Ao final da sequencia, reinicia o processo
  if (StepCounter>=StepCount):
    StepCounter = 0
  if (StepCounter<0):
    StepCounter = StepCount

  #Delay para movimentar o motor
  time.sleep(WaitTime)