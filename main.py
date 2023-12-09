import multiprocessing
import random
import time
import tkinter as tk
from tkinter import ttk, PhotoImage, font
import threading

import pygame

# import led


# Led shit adden.
#import led

# Flage und Bunker bauen.
pygame.init()
pygame.mixer.init()


def codeGen(x):
    var = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D"]
    tmp = []
    for g in range(0, x):
        tmp.append(var[random.randint(0, len(var) - 1)])
    return "".join(tmp)


stop = False
stopLock = False
stopBlue = False
stopRed = False
class logicWindow:

    def __init__(self):
        self.extraInput =[]
        #self.ledStuff = led.Led()
        self.blueCounting = False
        self.redCounting = False
        self.blueCounter = None
        self.redCounter = None
        self.redAmount = 0
        self.blueAmount = 0
        self.redTimeLable = None
        self.blueTimeLable = None
        self.mp = None
        self.stop = False
        self.inputLockThread = None
        self.blinker = None
        self.timeLable1 = None
        self.timeLable1 = None
        self.current1 = False
        self.counter2 = False
        # arm/defu labels
        self.timerLable = None
        self.armed = False
        self.infoLable = None
        self.armCode = None
        self.defCode = None
        self.armTries = 3
        self.outerBlinker = False
        self.bomTries = 3
        self.inputLock = False
        self.versucheLable = None
        self.inputLable = None
        self.p1 = None
        self.input = []
        self.fails = 1
        self.exitCode = 6969
        self.p1Sop = False
        # selection logic

        self.pressedKeys = []
        self.hoehe = [120, 220, 320]
        self.modie = ["Bombe", "Bunker", "Flage"]
        self.diffs = ["Easy", "Medium", "Hard"]
        self.times = [1, 10, 15]
        self.selectedGame = None
        self.selectedDiff = None
        self.selectedTime = None
        self.current = 0
        self.selection = -1
        self.game = None
        self.isInGame = False

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.focus_force()
        self.ev1 = self.root.bind("<KeyPress>", self.keydown)
        self.ev2 = self.root.bind("<KeyRelease>", self.keyup)
        self.root.title("Foxy´s Bombe")
        self.root.geometry("800x480")
        self.root.configure(background="black")
        tk.Label(self.root, name="text", text="Spielauswahl:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

        tk.Label(self.root, name="lable1", text="1:Bombe", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=120)
        tk.Label(self.root, name="lable2", text="2:Bunker", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                               y=220)
        tk.Label(self.root, name="lable3", text="3:Flagge", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=320)

        tk.Label(self.root, name="dont1", text="Rot: Zurück", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=0.0, rely=1.0, anchor='sw')
        tk.Label(self.root, name="dont2", text="Blau: Bestätigen", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=1.0, rely=1.0, anchor='se')

        self.selectLable = tk.Label(self.root, text="<--", bg="black", fg="green", font=("calibri light", 40))
        self.root.mainloop()

    def reset(self):
        global stop,stopRed,stopBlue
        self.extraInput = []
        self.clearFrame()

        stop = True
        try:
            self.mp.join()
        except Exception:
            pass

        #self.ledStuff.stopAllBlinkers()
        #self.ledStuff.turnOffAll()
        self.blueCounting = False
        self.redCounting = False
        stopRed = True
        try:
            self.redCounter.join()
        except Exception:
            pass
        stopRed = False

        stopBlue = True
        try:
            self.blueCounter.join()
        except Exception:
            pass
        stopBlue = False


        self.redAmount = 0
        self.blueAmount = 0
        self.armed = False
        self.mp = None
        stop = False
        self.inputLock = False
        self.selectedGame = None
        self.selectedDiff = None
        self.selectedTime = None
        self.isInGame = False
        self.input = []
        self.selectedGame = None
        self.current = 0
        self.selection = -1
        self.armTries = 3
        self.bomTries = 3

        tk.Label(self.root, name="text", text="Spielauswahl:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

        tk.Label(self.root, name="lable1", text="1:Bombe", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=120)
        tk.Label(self.root, name="lable2", text="2:Bunker", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                               y=220)
        tk.Label(self.root, name="lable3", text="3:Flagge", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=320)
        self.root.attributes("-fullscreen", True)
        tk.Label(self.root, name="dont1", text="Rot: Zurück", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=0.0, rely=1.0, anchor='sw')
        tk.Label(self.root, name="dont2", text="Blau: Bestätigen", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=1.0, rely=1.0, anchor='se')

        self.selectLable = tk.Label(self.root, text="<--", bg="black", fg="green", font=("calibri light", 40))

    def keydown(self, key):
        if key.keysym not in self.pressedKeys:
            self.pressedKeys.append(key.keysym)
            self.gameSelectInput(key)

    def keyup(self, key):
        if key.keysym in self.pressedKeys:
            self.pressedKeys.remove(key.keysym)

    def gameSelectInput(self, key):
        global stopRed,stopBlue
        if self.inputLock:
            return
        if not self.isInGame:
            if key.keysym in ["1", "2", "3"]:
                if self.selectedGame is None:

                    self.selection = int(key.char) - 1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
                elif self.selectedDiff is None:

                    self.selection = int(key.char) - 1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
                elif self.selectedTime is None:

                    self.selection = int(key.char) - 1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
            elif key.keysym == "Return" and self.selection in range(0, 3):
                if self.current == 0:
                    self.selectLable.place(x=1111, y=20000)
                    self.setLables(["1:Easy", "2:Medium", "3:Hard", "Schwirigkeit:"])
                    self.selectedGame = self.modie[self.selection]
                    self.selection = -1
                    self.current = self.current + 1
                elif self.current == 1:
                    self.selectLable.place(x=1000, y=213123)
                    self.setLables(["1:5Min", "2:10Min", "3:15Min", "Zeit:"])
                    self.selectedDiff = self.diffs[self.selection]
                    self.selection = -1
                    self.current = self.current + 1
                elif self.current == 2:
                    self.selectLable.place(x=1000, y=123123)
                    self.selectedTime = self.times[self.selection]

                    self.clearFrame()
                    self.startGame()
            elif key.keysym == "Delete":
                if self.current == 1:
                    self.setLables(["1:Bomb", "2:Bunker", "3:Flagge", "Spielauswahl:"])
                    self.current = self.current - 1
                    self.selection = -1
                    self.selectLable.place(x=1000, y=1200)
                    self.selectedGame = None
                elif self.current == 2:
                    self.setLables(["1:Easy", "2:Medium", "3:Hard", "Schwirigkeit:"])
                    self.current = self.current - 1
                    self.selection = -1
                    self.selectLable.place(x=1000, y=123123)
                    self.selectedDiff = None
        else:
            if self.selectedGame == "Bombe":
                if key.keysym == "Delete":
                    self.input = []
                    self.inputLable.configure(text="")
                elif key.keysym == "Return":
                    if not self.armed:
                        if "".join(self.input) == self.armCode:
                            self.armed = True
                            self.input = []
                            self.defuseBomb()
                        else:
                            self.reduceTries()
                    else:
                        if "".join(self.input) == self.defCode:
                            self.input = []

                            self.bombDefused()
                        else:

                            self.reduceTries()
                else:
                    self.input.append(key.keysym)
                    self.inputLable.configure(text="".join(self.input))
            elif self.selectedGame == "Flage":
                if key.keysym == "Delete":
                    self.input = []
                    #led red
                    #led blue off
                    self.infoLable.configure(text="RED")
                elif key.keysym == "Return":
                    if "".join(self.input) == "6969":
                        self.reset()
                    self.infoLable.configure(text="BLUE")
                    # led red off
                    # led blue
                else:
                    self.input.append(key.keysym)
            elif self.selectedGame == "Bunker":
                if key.keysym == "Delete":
                    self.input = []
                    # led red
                    # led blue off
                    stopBlue = True
                    try:
                        self.blueCounter.join()
                    except Exception:
                        pass
                    stopBlue = False
                    if not self.redCounting:
                        self.redCounter = threading.Thread(target=self.redTimer,daemon=True)
                        self.redCounter.start()
                elif key.keysym == "Return":
                    if "".join(self.input) == "6969":
                        self.reset()
                    stopRed = True
                    try:
                        self.redCounter.join()
                    except Exception:
                        pass
                    stopRed = False
                    if not self.blueCounting:
                        self.blueCounter = threading.Thread(target=self.blueTimer, daemon=True)
                        self.blueCounter.start()
                    # led red off
                    # led blue
                else:
                    self.input.append(key.keysym)
    def playAudio(self,name):
        pos = ["Boom"]
        print(name)
        if name == "Boom":
            file = "explosion.mp3"
            print("selected file")
        if name in pos:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

    def startGame(self):
        if self.selectedGame == "Bombe":
            self.isInGame = True
            self.armCode = codeGen(1)
            self.defCode = codeGen(1)
            self.armBomb()
            self.armTries = 3
        elif self.selectedGame == "Bunker":
            self.isInGame = True
            self.bunker()
        elif self.selectedGame == "Flage":
            print("hello")
            self.isInGame = True
            self.flage()

    def clearFrame(self):
        for wi in self.root.winfo_children():
            wi.destroy()

    def clearFrameCarfull(self):
        for wi in self.root.winfo_children():
            if str(wi) not in [".dont1", ".dont2"]:
                wi.destroy()

    def setLables(self, x):
        for wi in self.root.winfo_children():
            if str(wi) == ".lable1":
                wi.configure(text=x[0])
            elif str(wi) == ".lable2":
                wi.configure(text=x[1])
            elif str(wi) == ".lable3":
                wi.configure(text=x[2])
            elif str(wi) == ".text":
                wi.configure(text=x[3])

    def getLableWidght(self, key):
        if key.char == '1':
            for wi in self.root.winfo_children():
                if str(wi) == ".lable1":
                    return [wi.winfo_width(), wi.winfo_height()]
        if key.char == '2':
            for wi in self.root.winfo_children():
                if str(wi) == ".lable2":
                    return [wi.winfo_width(), wi.winfo_height()]
        if key.char == '3':
            for wi in self.root.winfo_children():
                if str(wi) == ".lable3":
                    return [wi.winfo_width(), wi.winfo_height()]

    def armBomb(self):
        self.clearFrame()
        #self.ledStuff.turnBlueOn()
        tk.Label(self.root, fg="green", bg="black", text="Bombe legen", font=("Ubuntu", 50)).pack()
        tk.Label(self.root, fg="green", bg="black", text="Code:", font=("Ubuntu", 15)).place(x=20, y=160)
        tk.Label(self.root, fg="green", bg="black", text=self.armCode, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Eingabe:", font=("Ubuntu", 30)).place(x=10, y=220)
        tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)
        self.versucheLable = tk.Label(self.root, fg="green", bg="black", text=str(self.bomTries), font=("Ubuntu", 30))
        self.versucheLable.place(x=210, y=280)
        self.inputLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.inputLable.place(x=180, y=220)
        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)
        self.root.update()

    def defuseBomb(self):
        #self.ledStuff.stopAllBlinkers()
        #self.ledStuff.turnOffAll()


        #self.ledStuff.startBlueBlinker()

        #self.ledStuff.setRGB((0, 255, 0))
        self.clearFrame()
        self.timerLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 50))
        self.timerLable.pack()
        tk.Label(self.root, fg="green", bg="black", text="Code:", font=("Ubuntu", 15)).place(x=20, y=160)
        tk.Label(self.root, fg="green", bg="black", text=self.defCode, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Eingabe:", font=("Ubuntu", 30)).place(x=10, y=220)
        tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)
        self.versucheLable = tk.Label(self.root, fg="green", bg="black", text=str(self.armTries), font=("Ubuntu", 30))
        self.versucheLable.place(x=210, y=280)
        self.inputLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.inputLable.place(x=180, y=220)
        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)
        self.mp = threading.Thread(target=self.timer, daemon=True)
        self.mp.start()
        #self.ledStuff.startStripeBlinker(True)

    def timer(self):
        global stop
        ctime = self.selectedTime * 60
        while ctime and not stop:
            if stop:
                break
            if ctime == (self.selectedTime*60)/2:
                self.outerBlinker = True
                #self.ledStuff.startRedBlinker()
                #self.ledStuff.stopBlueBlinker()
                #if not self.ledStuff.getRedIsAlive():
                    #self.ledStuff.startRedBlinker()
                   # pass
            mins, secs = divmod(ctime, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.timerLable.configure(text=timeformat)
            time.sleep(1)
            ctime -= 1
        if ctime == 0:
            self.timerLable.configure(text="00:00")
            self.root.update()
            self.explosion()

    def explosion(self):
        global stop,stopLock

        #self.ledStuff.stopAllBlinkers()
        #self.ledStuff.turnOffAll()
        #self.ledStuff.turnRedOn()
        #self.ledStuff.pixelFill((255, 0, 0))
        self.infoLable.configure(text="Bombe ist explodiert")
        self.root.update()
        self.inputLock = True
        stop = True
        stopLock =True
        try:
            self.inputLockThread.join()
        except Exception:
            pass
        stopLock = False
        try:
            self.mp.join()
        except Exception:
            pass
        self.root.update()
        threading.Thread(target=self.playAudio, args=("Boom",)).start()
        time.sleep(20)
        self.reset()
        # play audio

    def reduceTries(self):
        if not self.armed:
            if self.bomTries - 1 > 0:
                self.bomTries = self.bomTries - 1
                self.versucheLable.configure(text=self.bomTries)
                self.infoLable.configure(
                    text="Falsche eingabe \n eingabe für: " + str(10 * (4 - self.bomTries + 1)) + "sekunden gespert")
                self.inputLockThread = threading.Thread(target=self.lockInput, args=(10 * (4 - self.armTries + 1),), daemon=True)
                self.inputLockThread.start()
            else:
                self.infoLable.configure(text="Zu viele versuche\n Bombe ist deaktiviert")
        else:
            if self.armTries - 1 > 0:
                self.armTries = self.armTries - 1
                self.versucheLable.configure(text=self.armTries)
                self.infoLable.configure(
                    text="Falsche eingabe \n eingabe für: " + str(10 * (4 - self.armTries + 1)) + " sekunden espert")
                self.inputLockThread = threading.Thread(target=self.lockInput, args=(10 * (4 - self.bomTries + 1),),
                                                        daemon=True)
                self.inputLockThread.start()
            else:
                self.infoLable.configure(text="Zu viele versuche\n Bombe ist explodiert")
                self.explosion()

    def lockInput(self, ctime):
        global stopLock
        self.inputLock = True
        i = 0
        #if not self.ledStuff.getRedIsAlive():
            #pass
            #self.ledStuff.startRedBlinker()
        while i < 2 and not stopLock:
            i = i + 1
            time.sleep(1)
            if stopLock:
                break
        self.inputLock = False
        if not self.outerBlinker:
            pass
            #self.ledStuff.stopRedBlinker()
        if not stopLock:
            self.infoLable.configure(text="")

    def flage(self):
        tk.Label(self.root, fg="green", bg="black", text="Flagge", font=("Ubuntu", 50)).pack()
        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 90))
        self.infoLable.place(x=200, y=200)


    def bombDefused(self):
        global stop
        self.infoLable.configure(text="Die Bombe wurde entschärft")
        #Leds green machen
        #Defuse sound abspielen
        stop = True
        try:
            self.mp.join()
        except Exception:
            pass
        self.root.update()
        time.sleep(20)
        self.reset()

    def redTimer(self):
        global stopRed
        ctime = self.redAmount
        self.redCounting = True
        while True:
            if stopRed:
                self.redAmount = ctime
                self.redCounting = False
                break
            mins, secs = divmod(ctime, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.redTimeLable.configure(text=timeformat)
            time.sleep(1)
            ctime += 1

    def blueTimer(self):
        global stopBlue
        self.blueCounting = True
        ctime = self.blueAmount
        while True:
            if stopBlue:
                self.blueCounting = False
                self.blueAmount = ctime
                break
            mins, secs = divmod(ctime, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.blueTimeLable.configure(text=timeformat)
            time.sleep(1)
            ctime += 1

    def bunker(self):
        self.clearFrame()
        tk.Label(self.root, fg="green", bg="black", text="Bunker:", font=("Ubuntu", 50)).pack()
        tk.Label(self.root, fg="green", bg="black", text="Blue:", font=("Ubuntu", 90)).place(x=10, y=180)
        #tk.Label(self.root, fg="green", bg="black", text=self.armCode, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Red:", font=("Ubuntu", 90)).place(x=25, y=340)
        #tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)

        self.blueTimeLable = tk.Label(self.root, fg="green", bg="black", text="00:00", font=("Ubuntu", 90))
        self.blueTimeLable.place(x=320, y=180)

        self.redTimeLable = tk.Label(self.root, fg="green", bg="black", text="00:00", font=("Ubuntu", 90))
        self.redTimeLable.place(x=320, y=340)

        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)
        self.root.update()

# time.sleep(4)
tmp = logicWindow()
