import multiprocessing
import random
import time
import tkinter as tk
from tkinter import ttk, PhotoImage, font
import threading

import pygame

# import led


# Led shit adden.
import led

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

class logicWindow:

    def __init__(self):

        self.ledStuff = led.Led()

        self.mp = None
        self.stop = False
        self.inputLockThread = None
        self.blinker = None
        self.timeLable1 = None
        self.timeLable1 = None
        self.counter1 = False
        self.counter2 = False
        # arm/defu labels
        self.timerLable = None
        self.armed = False
        self.infoLable = None
        self.armCode = None
        self.defCode = None
        self.armTries = 3
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
        tk.Label(self.root, name="text", text="Spiel4:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

        tk.Label(self.root, name="lable1", text="1:Bombe", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=120)
        tk.Label(self.root, name="lable2", text="2:Bunker", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                               y=220)
        tk.Label(self.root, name="lable3", text="3:Flage", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=320)

        tk.Label(self.root, name="dont1", text="Rot: Zurück", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=0.0, rely=1.0, anchor='sw')
        tk.Label(self.root, name="dont2", text="Blau: Bestätigen", fg="green", bg="black", font=("Ubuntu", 30)).place(
            relx=1.0, rely=1.0, anchor='se')

        self.selectLable = tk.Label(self.root, text="<--", bg="black", fg="green", font=("calibri light", 40))
        self.root.mainloop()

    def reset(self):
        global stop

        self.clearFrame()

        stop = True
        try:
            self.mp.join()
        except Exception:
            pass

        self.ledStuff.stopAllBlinkers()
        self.ledStuff.turnOffAll()

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

        tk.Label(self.root, name="text", text="Spielmodus:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

        tk.Label(self.root, name="lable1", text="1:Bombe", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                              y=120)
        tk.Label(self.root, name="lable2", text="2:Bunker", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
                                                                                                               y=220)
        tk.Label(self.root, name="lable3", text="3:Flage", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,
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
                    self.setLables(["1:Easy", "2:Medium", "3:Hard", "Schrigkeit"])
                    self.selectedGame = self.modie[self.selection]
                    self.selection = -1
                    self.current = self.current + 1
                elif self.current == 1:
                    self.selectLable.place(x=1000, y=213123)
                    self.setLables(["1:5Min", "2:10Min", "3:15Min", "Zeit"])
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
                    self.setLables(["1:Bomb", "2:Bunker", "3:Flag", "Modus:"])
                    self.current = self.current - 1
                    self.selection = -1
                    self.selectLable.place(x=1000, y=1200)
                    self.selectedGame = None
                elif self.current == 2:
                    self.setLables(["1:Easy", "2:Medium", "3:Hard", "Schrigkeit"])
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

                            self.reset()
                        else:

                            self.reduceTries()
                else:
                    self.input.append(key.keysym)
                    self.inputLable.configure(text="".join(self.input))

    def startGame(self):
        if self.selectedGame == "Bombe":
            self.isInGame = True
            self.armCode = codeGen(1)
            self.defCode = codeGen(1)
            self.armBomb()
            self.armTries = 3
        elif self.selectedGame == "Bunker":
            pass
            self.isInGame = True
            self.bunker()
        elif self.selectedGame == "Flage":
            pass
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
        self.ledStuff.startBlueBlinker()
        self.ledStuff.setRGB((0, 0, 255))
        self.ledStuff.startStripeBlinker()
        tk.Label(self.root, fg="green", bg="black", text="Bombe scharf stellen", font=("Ubuntu", 50)).pack()
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
        self.ledStuff.stopBlueBlinker()
        self.ledStuff.startRedBlinker()
        self.ledStuff.stopStripeBlinker()
        self.ledStuff.setRGB((255, 0, 0))
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
        self.ledStuff.startStripeBlinker()

    def timer(self):
        global stop
        ctime = self.selectedTime * 60
        while ctime and not stop:
            if stop:
                break
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
        self.infoLable.configure(text="Bombe ist explodiert")
        self.root.update()
        time.sleep(0.2)
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
        self.ledStuff.stopAllBlinkers()
        self.ledStuff.turnOffAll()
        self.ledStuff.turnRedOn()
        self.ledStuff.pixelFill((255, 0, 0))
        time.sleep(10)
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
                self.infoLable.configure(text="Bomb disabled to many tries")
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
                self.infoLable.configure(text="Bomb exploded to many defuse tries")
                self.explosion()

    def lockInput(self, ctime):
        global stopLock
        self.inputLock = True
        i = 0
        while i < 2 and not stopLock:
            i = i + 1
            time.sleep(1)
            if stopLock:
                break
        self.inputLock = False
        if not stopLock:
            self.infoLable.configure(text="")


# time.sleep(4)
tmp = logicWindow()
