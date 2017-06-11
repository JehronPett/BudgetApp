from tkinter import *

class Window:

    def __init__(self, title):
        self.root = Tk(title)
        self.title = title
        self.label = Label(self.root, text=title)
        self.label.pack()
        self.root.mainloop()
