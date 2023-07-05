import random
import time
import tkinter as tk
from tkinter import ttk, PhotoImage, font
import threading
from subprocess import call
import RPi.GPIO as GPIO
from armBomb import armBomb
from key import key


#Led shit adden.
#Flage und Bunker bauen.

def codeGen(x):
    var = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "*", "#"]
    tmp = []
    for g in range(0, x):
        tmp.append(var[random.randint(0, len(var) - 1)])
    return "".join(tmp)


class logicWindow:

    def __init__(self):
        threading.Thread(target=self.keyAdapter,daemon=True).start()
        self.timeLable1 = None
        self.timeLable1 = None
        self.counter1 = False
        self.counter2 = False
        # arm/defu labels
        self.timerLable = None
        self.armed = None
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
        #selection logic

        self.pressedKeys = []
        self.hoehe = [120, 220, 320]
        self.modie = ["Bombe", "Bunker", "Flage"]
        self.diffs = ["Easy", "Medium", "Hard"]
        self.times = [5, 10, 15]
        self.selectedGame = None
        self.selectedDiff = None
        self.selectedTime = None
        self.current = 0
        self.selection = -1
        self.game = None
        self.isInGame = False

        self.root = tk.Tk()
        #self.root.attributes("-fullscreen", True)
        self.ev1 = self.root.bind("<KeyPress>", self.keydown)
        self.ev2 = self.root.bind("<KeyRelease>", self.keyup)
        self.root.title("Foxy´s Bombe")
        self.root.geometry("800x480")
        self.root.configure(background="black")
        tk.Label(self.root, name="text",text="Spiel4:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

        tk.Label(self.root, name="lable1", text="1:Bombe", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,y=120)
        tk.Label(self.root, name="lable2", text="2:Bunker", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,y=220)
        tk.Label(self.root, name="lable3", text="3:Flage", bg="black", fg="green", font=("Ubuntu", 45)).place(x=150,y=320)

        tk.Label(self.root, name="dont1", text="Rot: Zurück", fg="green", bg="black", font=("Ubuntu", 30)).place(relx=0.0, rely=1.0, anchor='sw')
        tk.Label(self.root, name="dont2", text="Blau: Bestätigen", fg="green", bg="black", font=("Ubuntu", 30)).place(relx=1.0, rely=1.0, anchor='se')

        self.selectLable = tk.Label(self.root, text="<--", bg="black", fg="green", font=("calibri light", 40))
        self.root.mainloop()

    def reset(self):
        self.timeLable1 = None
        self.timeLable1 = None
        self.counter1 = False
        self.counter2 = False
        self.clearFrame()
        # arm/defu labels
        self.infoLable = None
        self.armCode = None
        self.defCode = None
        self.armTries = 3
        self.bomTries = 3
        self.inputLock = False
        self.armed = False
        self.versucheLable = None
        self.inputLable = None
        self.input = []
        self.fails = 1

        # selection logic

        self.pressedKeys = []
        self.hoehe = [120, 220, 320]

        self.selectedGame = None
        self.selectedDiff = None
        self.selectedTime = None
        self.current = 0
        self.selection = -1
        self.game = None
        self.isInGame = False

        tk.Label(self.root, name="text",text="Spielmodus:", bg="black", fg="green", font=("Ubuntu", 50)).pack()

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
    def keydown(self, key):
        if key.keysym not in self.pressedKeys:
            self.pressedKeys.append(key.keysym)
            self.gameSelectInput(key)

    def keyup(self, key):
        if key.keysym in self.pressedKeys:
            self.pressedKeys.remove(key.keysym)

    def gameSelectInput(self, key):
        print(key.keysym)
        if not self.isInGame:
            if key.keysym in ["1","2","3"]:
                if self.selectedGame is None:
                    print("Game")
                    self.selection = int(key.char)-1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160+self.getLableWidght(key)[0],y=self.hoehe[int(key.char)-1])
                elif self.selectedDiff is None:
                    print("diff")
                    self.selection = int(key.char) - 1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
                elif self.selectedTime is None:
                    print("time")
                    self.selection = int(key.char) - 1
                    self.selectLable.configure(text="<--")
                    self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
            elif key.keysym == "Return" and self.selection in range(0,3):
                if self.current == 0:
                    self.selectLable.place(x=1000)
                    self.setLables(["1:Easy","2:Medium","3:Hard","Schrigkeit"])
                    self.selectedGame = self.modie[self.selection]
                    self.selection = -1
                    self.current = self.current+1
                elif self.current == 1:
                    self.selectLable.place(x=1000)
                    self.setLables(["1:5Min", "2:10Min", "3:15Min","Zeit"])
                    self.selectedDiff = self.diffs[self.selection]
                    self.selection = -1
                    self.current = self.current + 1
                elif self.current == 2:
                    self.selectLable.place(x=1000)
                    self.selectedTime = self.times[self.selection]
                    print(self.selectedGame,self.selectedDiff,self.selectedTime)
                    self.clearFrame()
                    self.startGame()
            elif key.keysym == "Delete":
                if self.current == 1:
                    self.setLables(["1:Bomb", "2:Bunker", "3:Flag","Modus:"])
                    self.current = self.current-1
                    self.selection = -1
                    self.selectLable.place(x=1000)
                    self.selectedGame = None
                elif self.current == 2:
                    self.setLables(["Easy", "Medium", "Hard","Schrigkeit"])
                    self.current = self.current-1
                    self.selection = -1
                    self.selectLable.place(x=1000)
                    self.selectedDiff = None
        else:
            if self.selectedGame == "Bombe":
                if key.char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "*", "#"]:
                    if key.char == "/":
                        self.input.append("#")
                    else:
                        self.input.append(key.char)
                    self.inputLable.configure(text="".join(self.input))
                elif key.keysym == "Return":
                    if "".join(self.input) == self.armCode or "".join(self.input) == self.defCode:
                        if not self.armed:
                            self.armed = True
                            self.input = []
                            self.defCode = codeGen(1)
                            self.defuseBomb()
                        else:
                            self.p1Sop = True
                    else:
                        if not self.armed:
                            self.reduceArmTries()
                            self.input = []
                            self.inputLable.configure(text="")
                        else:
                            pass
                elif key.keysym == "Delete":
                    self.input = []
                    self.inputLable.configure(text="")
            elif self.selectedGame == "Bunker":
                if key.keysym in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "*", "#"]:
                    if key.char == "/":
                        self.input.append("#")
                    else:
                        self.input.append(key.char)
                elif key.keysym == "Delete":
                    self.counter1 = True
                    self.counter2 = False
                    self.input = []
                elif key.keysym == "Return":
                    self.counter2= True
                    self.counter1 = False
                    if "".join(self.input) == str(self.exitCode):
                        self.reset()
            elif self.selectedGame == "Flage":
                if key.keysym in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "*", "#"]:
                    if key.char == "/":
                        self.input.append("#")
                    else:
                        self.input.append(key.char)
                elif key.keysym == "Delete":
                    self.setFlagText("red")
                    self.input=[]
                elif key.keysym == "Return":
                    self.setFlagText("blue")
                    if "".join(self.input) == str(self.exitCode):
                        self.reset()

    def keyAdapter(self):
        out = ["delete", "enter"]

        butonsIn = [19, 6]
        butonsOut = [26, 13]
        inputs = [4, 17, 27, 22]
        outputs = [24, 25, 12, 16]

        matrix = [["1", "2", "3", "A"],
                  ["4", "5", "6", "B"],
                  ["7", "8", "9", "C"],
                  ["*", "0", "#", "D"]]

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
                        self.gameSelectInput(key(matrix[outputs.index(x)][inputs.index(y)],matrix[outputs.index(x)][inputs.index(y)]))
                        while GPIO.input(y):
                            time.sleep(0.2)
                GPIO.output(int(x), False)

            for x in butonsOut:
                GPIO.output(int(x), True)
                for y in butonsIn:
                    if GPIO.input(y):
                        # print(out[butonsOut.index(x)])
                        self.gameSelectInput(key("",out[butonsOut.index(x)]))
                        while GPIO.input(y):
                            time.sleep(0.2)
                GPIO.output(int(x), False)

    def startGame(self):
        if self.selectedGame == "Bombe":
            self.isInGame = True
            self.armCode = codeGen(1)
            self.defCode = codeGen(1)
            self.armBomb()
        elif self.selectedGame == "Bunker":
            self.isInGame = True
            self.bunker()
        elif self.selectedGame == "Flage":
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
        tk.Label(self.root, fg="green", bg="black", text="Bombe scharf stellen", font=("Ubuntu", 50)).pack()
        tk.Label(self.root, fg="green", bg="black", text="Code:", font=("Ubuntu", 15)).place(x=20, y=160)
        tk.Label(self.root, fg="green", bg="black", text=self.armCode, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Eingabe:", font=("Ubuntu", 30)).place(x=10, y=220)
        tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)
        self.versucheLable = tk.Label(self.root, fg="green", bg="black", text=str(self.armTries), font=("Ubuntu", 30))
        self.versucheLable.place(x=210, y=280)

        self.inputLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.inputLable.place(x=180, y=220)

        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)

    def reduceArmTries(self):
        if self.armTries > 0:
            self.armTries = self.armTries - 1
            self.infoLable.configure(text="Falsche " + str(self.fails * 30) + "s sperre")
            self.versucheLable.configure(text=self.armTries)
            threading.Thread(target=self.lockInput, daemon=True).start()
            self.fails += 1
        else:
            time.sleep(120)
            self.reset()


    def lockInput(self):
        self.inputLock = True
        time.sleep(self.fails * 1)
        self.inputLock = False

    def defuseBomb(self):
        self.clearFrame()
        self.timerLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 50))
        self.timerLable.pack()
        tk.Label(self.root, fg="green", bg="black", text="Code:", font=("Ubuntu", 15)).place(x=20, y=160)
        tk.Label(self.root, fg="green", bg="black", text=self.defCode, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Eingabe:", font=("Ubuntu", 30)).place(x=10, y=220)
        tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)
        self.versucheLable = tk.Label(self.root, fg="green", bg="black", text=str(self.bomTries), font=("Ubuntu", 30))
        self.versucheLable.place(x=210, y=280)

        self.inputLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.inputLable.place(x=180, y=220)

        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)
        self.p1 = threading.Thread(target=self.timer,daemon=True)
        self.p1.start()

    def timer(self):
        ctime = self.selectedTime*60
        while ctime:
            mins, secs = divmod(ctime, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.timerLable.configure(text=timeformat)
            time.sleep(1)
            ctime -= 1
            if self.p1Sop:
                ctime = False
        if not self.p1Sop:
            self.explosion()

    def explosion(self):
        print("boom")

    def flage(self):
        self.clearFrame()
        tk.Label(self.root,text="Keine Farbe",bg="black",fg="green",font=("Ubunutu",60)).pack()

    def setFlagText(self,x):
        self.clearFrame()
        tk.Label(self.root,text=x,bg="black",fg="green",font=("Ubuntu",60)).pack()

    def bunker(self):
        self.clearFrame()
        tk.Label(self.root,text="Bunker",bg="black",fg="green",font=("Ubuntu",60)).pack()
        tk.Label(self.root,text="Blau",bg="black",fg="green",font=("Ubuntu",60)).place(x=1,y=110)
        tk.Label(self.root,text="Rot",bg="black",fg="green",font=("Ubuntu",60)).place(x=550,y=110)
        self.timeLable1 = tk.Label(self.root,text="00:00",fg="green",bg="black",font=("Ubuntu",60))
        self.timeLable1.place(x=10,y=230)
        self.timeLable2 = tk.Label(self.root,text="00:00",fg="green",bg="black",font=("Ubuntu",60))
        self.timeLable2.place(x=550,y=230)
        threading.Thread(target=self.counterBlue,daemon=True).start()
        threading.Thread(target=self.counterRed,daemon=True).start()


    def counterBlue(self):#
        counter = 0
        while self.isInGame:
            time.sleep(1)
            if self.counter1:
                counter = counter+1
            mins, secs = divmod(counter, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.timeLable1.configure(text=timeformat)
        if counter > self.selectedTime * 60:
            print("Blue Wins")
            tk.Label(self.root,text="Blau hat gewonnen",fg="green",bg="black",font=("Ubuntu",30)).pack()
            self.counter1 = False
            self.counter2 = False
    def counterRed(self):
        counter = 0
        while self.isInGame:
            time.sleep(1)
            if self.counter2:
                counter = counter+1
            mins, secs = divmod(counter, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.timeLable2.configure(text=timeformat)
            if counter > self.selectedTime*60:
                print("Red Wins")
                tk.Label(self.root, text="Rot hat gewonnen", fg="green", bg="black", font=("Ubuntu", 30)).pack()
                self.counter1 = False
                self.counter2 = False


#threading.Thread(target=call,args=(["python","keyPadAdapter.py"],)).start()
tmp = logicWindow()