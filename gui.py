import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FALSE, LEFT, NORMAL, RIGHT, TRUE, VERTICAL, X, Y, END

def getDir(fld):
    location = filedialog.askdirectory()
    fld.delete(0,END)
    fld.insert(0,location)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")       # Width x height
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
    serverlbl.grid(row = 1, column = 0, sticky='we')
    folderlbl = ttk.Label(folderFrame,text="Honeypot Webpage Folderpath:",font=('Courier',13,'bold'))
    folderlbl.grid(row = 1, column = 0, sticky='we')
    loglbl = ttk.Label(logFrame,text="Logfile Folderpath:",font=('Courier',13,'bold'))
    loglbl.grid(row = 1, column = 0, sticky='we')

    # server = OptionMenu()
    # folderpath = Entry()
    # logfile = Entry()
    options = ["Apache", "Nginx"]
    clicked = tk.StringVar()
    clicked.set("Apache")
    serverfld = tk.OptionMenu(serverFrame, clicked, *options )
    serverfld.grid(row = 1, column = 1, sticky='we')
    folderfld = tk.Entry(folderFrame, text="")
    folderfld.grid(row = 1, column = 1, sticky='we')
    logfld = tk.Entry(logFrame, text="")
    logfld.grid(row = 1, column = 1, sticky='we')

    # Btn for directory locations
    folderBtn = tk.Button(folderFrame, text="Select directory", command=lambda:getDir(folderfld))
    folderBtn.grid(row = 1, column = 2, sticky='we')
    logBtn = tk.Button(logFrame, text="Select directory", command=lambda:getDir(logfld))
    logBtn.grid(row = 1, column = 2, sticky='we')

    

    root.mainloop()