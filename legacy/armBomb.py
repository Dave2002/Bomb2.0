import random
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage

import time


class armBomb():

    def __init__(self, root, code):
        self.root = root
        self.pressedKeys = []
        self.lock = False
        self.input = []
        self.code = code
        self.tries = 3
        self.fails = 1
        self.ev1 = self.root.bind("<KeyPress>", self.keydown)
        self.ev2 = self.root.bind("<KeyRelease>", self.keyup)
        tk.Label(self.root, fg="green", bg="black", text="Bombe scharf stellen", font=("Ubuntu", 50)).pack()
        tk.Label(self.root, fg="green", bg="black", text="Code:", font=("Ubuntu", 15)).place(x=20, y=160)
        tk.Label(self.root, fg="green", bg="black", text=self.code, font=("Ubuntu", 15)).place(x=100, y=160)
        tk.Label(self.root, fg="green", bg="black", text="Eingabe:", font=("Ubuntu", 30)).place(x=10, y=220)
        tk.Label(self.root, fg="green", bg="black", text="Versuche:", font=("Ubuntu", 30)).place(x=10, y=280)

        self.versucheLable = tk.Label(self.root, fg="green", bg="black", text=str(self.tries), font=("Ubuntu", 30))
        self.versucheLable.place(x=210, y=280)

        self.inputLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.inputLable.place(x=180, y=220)

        self.infoLable = tk.Label(self.root, fg="green", bg="black", text="", font=("Ubuntu", 30))
        self.infoLable.place(x=10, y=350)

    def keydown(self, key):
        if key.keysym not in self.pressedKeys:
            self.pressedKeys.append(key.keysym)
            self.inputHandler(key)

    def keyup(self, key):
        if key.keysym in self.pressedKeys:
            self.pressedKeys.remove(key.keysym)

    def inputHandler(self, key):
        print(key.char)
        if not self.lock:
            if key.keysym in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "*", "#"]:
                self.input.append(key.keysym)
                self.inputLable.configure(text="".join(self.input))
            elif key.keysym == "Return":
                if "".join(self.input) == self.code:
                    pass
                else:
                    self.reduceTries()
            elif key.keysym == "Delete":
                self.inputLable.configure(text="")
                self.input = []

    def reduceTries(self):
        if self.tries > 0:
            self.tries = self.tries - 1
            self.infoLable.configure(text="Falsche " + str(self.fails * 30) + "s sperre")
            self.versucheLable.configure(text=self.tries)
            threading.Thread(target=self.lockInput, daemon=True).start()
            self.fails += 1

    def isAlive(self):
        if self.tries > 0:
            return True
        else:
            return False

    def lockInput(self):
        self.lock = True
        time.sleep(self.fails * 1)
        self.lock = False

    def kill(self):
        self.__del__()

    def __del__(self):
        try:
            self.root.unbind("<KeyPress>", self.ev1)
        except:
            pass
        try:
            self.root.unbind("<KeyRelease>", self.ev2)
        except:
            pass
        del self
