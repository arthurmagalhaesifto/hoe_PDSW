#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use Pins 18, 22, 24, 26 (GPIO24, GPIO25, GPIO8, GPIO7)
StepPins = [24, 25, 8, 7]

# Set all pins as output
for pin in StepPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Define some settings
WaitTime = 0.001

# Define half-step sequence
StepCount = 8
Seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

def perform_steps(nb):
    StepCounter = 0
    if nb < 0:
        sign = -1
    else:
        sign = 1
    nb = sign * nb * 2  # times 2 because half-step
    for i in range(nb):
        for pin in range(4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        StepCounter += sign
        # If we reach the end of the sequence, start again
        if StepCounter == StepCount:
            StepCounter = 0
        if StepCounter < 0:
            StepCounter = StepCount - 1
        # Wait before moving on
        time.sleep(WaitTime)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        steps = int(request.form['steps'])
        perform_steps(steps)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
