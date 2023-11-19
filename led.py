#include all necessary packages to get LEDs to work with Raspberry Pi
import time
from legacy import board
import neopixel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

stop = False
def ledOutSideBlink(c):
    if c == "blue":
        outsideBlueOn()
        time.sleep(1)
        outsideBlueOff()
    else:
        outsideRedOn()
        time.sleep(1)
        outsideRedOff()
def outsideRedOn():
    GPIO.output(20,True)
    #18 -> 20
def outsideRedOff():
    GPIO.output(20,False)

def outsideBlueOn():
    GPIO.output(23,True)

def outsideBlueOff():
    GPIO.output(23,False)

pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

def green():
    pixels1.fill((0,255,0))
    print("test")
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


def off():
    pixels1.fill((0,0,0))

def blink(intervall,color):
    while not stop:
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

