import RPi.GPIO as GPIO
import time
#from pynput.keyboard import Key, Controller
import pyautogui

#keyboard = Controller()

out = ["delete", "enter"]

butonsIn = [19, 6]
butonsOut = [26, 13]
inputs = [4, 17, 27, 22]
outputs = [24, 25, 12, 16]

matrix = [["1", "2", "3", "A"],
          ["4", "5", "6", "B"],
          ["7", "8", "9", "C"],
          ["*", "0", "/", "D"]]


def sendKey(key):
    with pyautogui.hold(key):
        pyautogui.sleep(0.1)


GPIO.setmode(GPIO.BCM)

for x in outputs:
    GPIO.setup(int(x), GPIO.OUT)

for x in butonsOut:
    GPIO.setup(int(x), GPIO.OUT)
    GPIO.output(int(x), True)

for g in inputs:
    GPIO.setup(int(g), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for g in butonsIn:
    GPIO.setup(int(g), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    for x in outputs:
        GPIO.output(int(x), True)
        for y in inputs:
            if GPIO.input(y):
                #print(matrix[outputs.index(x)][inputs.index(y)])
                sendKey(matrix[outputs.index(x)][inputs.index(y)])
                while GPIO.input(y):
                    time.sleep(0.2)
        GPIO.output(int(x), False)

    for x in butonsOut:
        GPIO.output(int(x), True)
        for y in butonsIn:
            if GPIO.input(y):
                #print(out[butonsOut.index(x)])
                sendKey(out[butonsOut.index(x)])
                while GPIO.input(y):
                    time.sleep(0.2)
        GPIO.output(int(x), False)
