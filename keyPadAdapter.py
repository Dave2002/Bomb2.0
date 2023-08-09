import RPi.GPIO as GPIO
import time
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Set the Row Pins
ROW_1 = 24
ROW_2 = 25
ROW_3 = 12
ROW_4 = 16

# Set the Column Pins
COL_1 = 4
COL_2 = 17
COL_3 = 27
COL_4 = 22

GPIO.setwarnings(False)
# BCM numbering
GPIO.setmode(GPIO.BCM)

# Set Row pins as output
GPIO.setup(ROW_1, GPIO.OUT)
GPIO.setup(ROW_2, GPIO.OUT)
GPIO.setup(ROW_3, GPIO.OUT)
GPIO.setup(ROW_4, GPIO.OUT)

# Set column pins as input and Pulled up high by default
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sendKey(x):
    keyboard.press(x)
    time.sleep(0.1)
    keyboard.release(x)
def wait_for(x):
    while GPIO.input(x) == GPIO.LOW:
        time.sleep(0.05)
# function to read each row and each column
def readRow(line, characters):
    GPIO.output(line, GPIO.LOW)
    if GPIO.input(COL_1) == GPIO.LOW:
        sendKey(characters[0])
        wait_for(COL_1)
    if GPIO.input(COL_2) == GPIO.LOW:
        sendKey(characters[1])
        wait_for(COL_2)
    if GPIO.input(COL_3) == GPIO.LOW:
        sendKey(characters[2])
        wait_for(COL_3)
    if GPIO.input(COL_4) == GPIO.LOW:
        sendKey(characters[3])
        wait_for(COL_4)
    GPIO.output(line, GPIO.HIGH)


# Endless loop by checking each row
try:
    while True:
        readRow(ROW_1, ["1","2","3","A"])
        readRow(ROW_2, ["4","5","6","B"])
        readRow(ROW_3, ["7","8","9","C"])
        readRow(ROW_4, ["*","0","#","D"])
        time.sleep(0.1) # adjust this per your own setup
except KeyboardInterrupt:
    print("\nKeypad Application Interrupted!")
    GPIO.cleanup()