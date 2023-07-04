#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
def outsideBlueOn():
    GPIO.output(18,True)

def outsideBlueOff():
    GPIO.output(18,False)

def outsideRedOn():
    GPIO.output(23,True)

def outsideRedOff():
    GPIO.output(23,False)

pixels1 = neopixel.NeoPixel(board.D21, 55, brightness=1)

def green():
    pixels1.fill((0,255,0))

def red():
    pixels1.fill((255, 0, 0))

def blue():
    pixels1.fill((0, 0, 255))

def yellow():
    pixels1.fill((255,255,0))

def puls(intervall):
    for x in range(0, 250, intervall):
        pixels1.fill((0, x, 0))
        time.sleep(0.1)
    for g in range(250,0,-intervall):
        pixels1.fill((0,x,0))
        time.sleep(0.1)
    pixels1.fill((0,0,0))

def blink(intervall,color):
    while True:
        if color == "green":
            green()
        elif color == "red":
            red()
        elif color == "yellow":
            yellow()
        elif color == "blue":
            blue()
        time.sleep(intervall/2)
        pixels1.fill((0,0,0))
        time.sleep(intervall/2)

outsideBlueOn()
time.sleep(2)
outsideBlueOff()
outsideRedOn()
time.sleep(2)
outsideRedOff()
