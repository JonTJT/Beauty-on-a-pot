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
    if srcIntVar.get() == 1:
        source = None
        root_ext = os.path.splitext("default.html")
    else:
        if source == "":
            print("No input found")
            return
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

def disableEntry():
    if srcIntVar.get() == 1:
        srcfld.delete(0,END)
        srcfld["state"] = DISABLED
        srcBtn["state"] = DISABLED
    if srcIntVar.get() == 0:
        srcfld["state"] = NORMAL
        srcBtn["state"] = NORMAL


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")       # Width x height
    root.title("Beauty On a Pot")
    root.resizable(0,0)

    MainTitle = ttk.Label(root, text='Beauty On a Pot' , font=('Aquire',22,'bold'))
    MainTitle.pack()

    topLeftFrame = tk.Frame(root)
    topLeftFrame.place(relwidth=0.45, relheight=0.3, rely=0.2, relx=0.05)
    bottomLeftFrame = tk.Frame(root)
    bottomLeftFrame.place(relwidth=0.45, relheight=0.3, rely=0.4, relx=0.05)

    topRightFrame = tk.Frame(root)
    topRightFrame.place(relwidth=0.45, relheight=0.3, rely=0.2, relx=0.50)
    bottomRightFrame = tk.Frame(root)
    bottomRightFrame.place(relwidth=0.45, relheight=0.3, rely=0.4, relx=0.50)

    # server = OptionMenu()
    serverlbl = ttk.Label(topLeftFrame,text="Select web server:",font=('Courier',13,'bold'))
    serverlbl.grid(row = 0, column = 0, sticky='ew')
    options = ["Apache", "Nginx"]
    clicked = tk.StringVar()
    clicked.set("Apache")
    serverfld = tk.OptionMenu(topLeftFrame, clicked, *options )
    serverfld.grid(row = 0, column = 1, sticky='ew')

    # logfile = Entry()
    loglbl = ttk.Label(bottomLeftFrame,text="Logfile Folderpath:",font=('Courier',13,'bold'))
    loglbl.grid(row = 0, column = 0)
    logfld = tk.Entry(bottomLeftFrame, text="")
    logfld.grid(row = 1, column = 0, sticky='ew')
    logBtn = tk.Button(bottomLeftFrame, text="Select directory", command=lambda:getDir(logfld))
    logBtn.grid(row = 2, column = 0, sticky='w')

    # server = OptionMenu()
    templatelbl = ttk.Label(topRightFrame,text="Honeypot Template:",font=('Courier',13,'bold'))
    templatelbl.grid(row = 0, column = 0, sticky='we')
    templateOptions = ["Login", "Search"]
    templateClicked = tk.StringVar()
    templateClicked.set("Login")
    templatefld = tk.OptionMenu(topRightFrame, templateClicked, *templateOptions )
    templatefld.grid(row = 0, column = 1, sticky='we')

    # srcfield = Entry()
    extraFrame = tk.Frame(bottomRightFrame)
    extraFrame.grid(row = 0, sticky='w')
    srclbl = ttk.Label(extraFrame,text="Source File:",font=('Courier',13,'bold'))
    srclbl.grid(row = 0, column = 0, sticky='w')
    srcIntVar = tk.IntVar()
    srcDefaultBtn = tk.Checkbutton(extraFrame, text="Default", command=disableEntry, variable=srcIntVar, onvalue=1, offvalue=0)
    srcDefaultBtn.grid(row = 0, column = 1, sticky='w', padx=10)
    srcfld = tk.Entry(bottomRightFrame, text="", width=43)
    srcfld.grid(row = 1, column = 0, sticky='w')
    srcBtn = tk.Button(bottomRightFrame, text="Select Source File", command=lambda:getSrc(srcfld))
    srcBtn.grid(row = 2, column = 0, sticky='w')


    genBtn = tk.Button(root, text="Generate", command=lambda:generate())
    genBtn.place(rely=0.7, relx=0.67)

    root.mainloop()