import func as fn
import os
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FALSE, LEFT, NORMAL, RIGHT, TRUE, VERTICAL, X, Y, END

def generate():
    fn.server = clicked.get()
    fn.logfile = logfld.get()

    source = srcfld.get()
    root_ext = ""
    if source == "":
        root_ext = os.path.splitext("default.html")
    else:
        root_ext = os.path.splitext(source)

    template = ""
    outputFile = ""
    if templateClicked.get() == "Login":
        template = "AdminLoginPageTemplate.html"
        outputFile = root_ext[0] + "_AdminLoginHoneypot" + root_ext[1]
    elif templateClicked.get() == "Search":
        template = "SecretSearchPage.html"
        outputFile = root_ext[0] + "_SearchHoneypot" + root_ext[1]
    
    fn.generateHoneypotPage(template, source, outputFile)

def getDir(fld):
    location = filedialog.askdirectory()
    fld.delete(0,END)
    fld.insert(0,location)

def getSrc(fld):
    srcFile = filedialog.askopenfilename()
    fld.delete(0,END)
    fld.insert(0,srcFile)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")       # Width x height
    root.title("Beauty On a Pot")
    MainTitle = ttk.Label(root, text='Beauty On a Pot' , font=('Aquire',22,'bold'))
    MainTitle.pack()
    serverFrame = tk.Frame(root)
    serverFrame.pack()
    logFrame = tk.Frame(root)
    logFrame.pack()
    templateFrame = tk.Frame(root)
    templateFrame.pack()
    srcFrame = tk.Frame(root)
    srcFrame.pack()

    # Labels
    serverlbl = ttk.Label(serverFrame,text="Server:",font=('Courier',13,'bold'))
    serverlbl.grid(row = 1, column = 0, sticky='e')
    loglbl = ttk.Label(logFrame,text="Logfile Folderpath:",font=('Courier',13,'bold'))
    loglbl.grid(row = 1, column = 0, sticky='e')
    templatelbl = ttk.Label(templateFrame,text="Honeypot Template:",font=('Courier',13,'bold'))
    templatelbl.grid(row = 1, column = 0, sticky='e')
    srclbl = ttk.Label(srcFrame,text="Source File:",font=('Courier',13,'bold'))
    srclbl.grid(row = 1, column = 0, sticky='e')

    # server = OptionMenu()
    # logfile = Entry()
    options = ["Apache", "Nginx"]
    clicked = tk.StringVar()
    clicked.set("Apache")
    serverfld = tk.OptionMenu(serverFrame, clicked, *options )
    serverfld.grid(row = 1, column = 1, sticky='e')
    logfld = tk.Entry(logFrame, text="")
    logfld.grid(row = 1, column = 1, sticky='e')

    templateOptions = ["Login", "Search"]
    templateClicked = tk.StringVar()
    templateClicked.set("Login")
    templatefld = tk.OptionMenu(templateFrame, templateClicked, *templateOptions )
    templatefld.grid(row = 1, column = 1, sticky='e')
    srcfld = tk.Entry(srcFrame, text="")
    srcfld.grid(row = 1, column = 1, sticky='e')

    # Btn for directory locations
    logBtn = tk.Button(logFrame, text="Select directory", command=lambda:getDir(logfld))
    logBtn.grid(row = 1, column = 2, sticky='e')
    
    srcBtn = tk.Button(srcFrame, text="Select Source File", command=lambda:getSrc(srcfld))
    srcBtn.grid(row = 1, column = 2, sticky='e')

    genBtn = tk.Button(root, text="Generate", command=lambda:generate())
    genBtn.pack()
    
    root.mainloop()