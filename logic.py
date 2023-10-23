import tkinter as tk

class logicWindow:

    def __init__(self):
        #selection logic
        self.titles = ["Modie","Diff","Zeit"]
        self.pressedKeys = []
        self.hoehe = [120, 220, 320]
        self.selections = [["Bombe", "Bunker", "Flagge"],["Easy", "Medium", "Hard"],[1, 10, 15]]
        self.currentselections = []
        self.current = 0
        self.selection = -1
        self.game = None
        self.isInGame = False

        self.root = tk.Tk()
        #self.root.attributes("-fullscreen", True)
        self.root.focus_force()
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


    def keydown(self, key):
        if key.keysym not in self.pressedKeys:
            self.pressedKeys.append(key.keysym)
            self.gameSelectInput(key)

    def keyup(self, key):
        if key.keysym in self.pressedKeys:
            self.pressedKeys.remove(key.keysym)

    def gameSelectInput(self,key):
        if key.keysym in ["1","2","3"]:
            self.selection = int(key.char) - 1
            self.selectLable.configure(text="<--")
            self.selectLable.place(x=160 + self.getLableWidght(key)[0], y=self.hoehe[int(key.char) - 1])
        if key.keysym == "BackSpace":
            if len(self.currentselections) != 0:
                self.currentselections.pop()
                self.selection = -1
                self.setLables(self.selections[len(self.currentselections)], self.titles[len(self.currentselections)])
        if key.keysym == "Return":
            self.currentselections.append(self.selections[len(self.currentselections)][self.selection])
            self.selection = -1
            self.setLables(self.selections[len(self.currentselections)],self.titles[len(self.currentselections)])

    def clearFrame(self):
        for wi in self.root.winfo_children():
            wi.destroy()

    def clearFrameCarfull(self):
        for wi in self.root.winfo_children():
            if str(wi) not in [".dont1", ".dont2"]:
                wi.destroy()

    #Updates the four lables. Needs a String Array of the lenght of 4
    def setLables(self, x,y):
        for wi in self.root.winfo_children():
            if str(wi) == ".lable1":
                wi.configure(text=x[0])
            elif str(wi) == ".lable2":
                wi.configure(text=x[1])
            elif str(wi) == ".lable3":
                wi.configure(text=x[2])
            elif str(wi) == ".text":
                wi.configure(text=y)

    def getLableWidght(self, key):
        key = int(key.char)
        if key == 1:
            for wi in self.root.winfo_children():
                if str(wi) == ".lable1":
                    return [wi.winfo_width(), wi.winfo_height()]
        if key == 2:
            for wi in self.root.winfo_children():
                if str(wi) == ".lable2":
                    return [wi.winfo_width(), wi.winfo_height()]
        if key == 3:
            for wi in self.root.winfo_children():
                if str(wi) == ".lable3":
                    return [wi.winfo_width(), wi.winfo_height()]


lo = logicWindow()