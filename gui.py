import func as fn
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FALSE, LEFT, NORMAL, RIGHT, TRUE, VERTICAL, X, Y, END

def generate():
    fn.server = clicked.get()
    fn.folderpath = folderfld.get()
    fn.logfile = logfld.get()
    fn.genFiles()

def getDir(fld):
    location = filedialog.askdirectory()
    fld.delete(0,END)
    fld.insert(0,location)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")       # Width x height
    root.title("Beauty On a Pot")
    MainTitle = ttk.Label(root, text='Beauty On a Pot' , font=('Aquire',22,'bold'))
    MainTitle.pack()
    serverFrame = tk.Frame(root)
    serverFrame.pack()
    folderFrame = tk.Frame(root)
    folderFrame.pack()
    logFrame = tk.Frame(root)
    logFrame.pack()

    # Labels
    serverlbl = ttk.Label(serverFrame,text="Server:",font=('Courier',13,'bold'))
    serverlbl.grid(row = 1, column = 0, sticky='e')
    folderlbl = ttk.Label(folderFrame,text="Honeypot Webpage Folderpath:",font=('Courier',13,'bold'))
    folderlbl.grid(row = 1, column = 0, sticky='e')
    loglbl = ttk.Label(logFrame,text="Logfile Folderpath:",font=('Courier',13,'bold'))
    loglbl.grid(row = 1, column = 0, sticky='e')

    # server = OptionMenu()
    # folderpath = Entry()
    # logfile = Entry()
    options = ["Apache", "Nginx"]
    clicked = tk.StringVar()
    clicked.set("Apache")

    serverfld = tk.OptionMenu(serverFrame, clicked, *options )
    serverfld.grid(row = 1, column = 1, sticky='e')
    folderfld = tk.Entry(folderFrame, text="")
    folderfld.grid(row = 1, column = 1, sticky='e')
    logfld = tk.Entry(logFrame, text="")
    logfld.grid(row = 1, column = 1, sticky='e')

    # Btn for directory locations
    folderBtn = tk.Button(folderFrame, text="Select directory", command=lambda:getDir(folderfld))
    folderBtn.grid(row = 1, column = 2, sticky='e')
    logBtn = tk.Button(logFrame, text="Select directory", command=lambda:getDir(logfld))
    logBtn.grid(row = 1, column = 2, sticky='e')

    logBtn = tk.Button(root, text="Generate", command=lambda:generate())
    logBtn.pack()

    root.mainloop()