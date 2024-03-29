import func as fn
import os
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import Message, Widget, filedialog , messagebox , ttk
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, FALSE, LEFT, NORMAL, RIGHT, TRUE, VERTICAL, X, Y, END
import time

def insertConsole(text):
    textconsole["state"] = NORMAL
    textconsole.insert(END, text + "\n")
    textconsole["state"] = DISABLED

def generateReport():
    try:
        logfile = logfld.get() + "/honeypot.log"
        if clicked.get() == "Apache":
            fn.ApacheGenerateReport(logfile)
        elif clicked.get() == "Nginx":
            fn.NginxGenerateReport(logfile)
    except IOError:
        insertConsole("ERROR: Unable to generate report csv file.")

def generate():
    fn.server = clicked.get()
    fn.logfile = logfld.get()

    try:
        if not os.path.exists(fn.logfile):
            print("ERROR: Directory does not exist for Logfile.")
            insertConsole("ERROR: Directory does not exist for Logfile.")
            return
    except IOError:
        print("ERROR: Unable to set logfile path.")
        insertConsole("ERROR: Unable to set logfile path.")
        return

    source = srcfld.get()
    outputFileName = "default.html"
    if srcIntVar.get() == 1:
        source = None
    else:
        if not os.path.exists(source):
            print("ERROR: Source file not found.")
            insertConsole("ERROR: Source file not found.")
            return
        outputFileName = os.path.basename(source)

    curr_dir = os.getcwd()
    
    template = ""
    if templateClicked.get() == "Login":
        template = "AdminLoginPageTemplate.html"
        outputFile = curr_dir + "/AdminLoginHoneypot_" + outputFileName 
    elif templateClicked.get() == "Search":
        template = "SecretSearchPage.html"
        outputFile = curr_dir + "/SearchHoneypot_" + outputFileName
    
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
    root.geometry("600x400")       # Width x height
    root.title("Beauty On a Pot")
    root.resizable(0,0)

    MainTitle = ttk.Label(root, text='Beauty On a Pot' , font=('Aquire',22,'bold'))
    MainTitle.pack()

    topLeftFrame = tk.Frame(root)
    topLeftFrame.place(relwidth=0.45, relheight=0.3, rely=0.15, relx=0.05)
    bottomLeftFrame = tk.Frame(root)
    bottomLeftFrame.place(relwidth=0.45, relheight=0.3, rely=0.3, relx=0.05)

    topRightFrame = tk.Frame(root)
    topRightFrame.place(relwidth=0.45, relheight=0.3, rely=0.15, relx=0.55)
    bottomRightFrame = tk.Frame(root)
    bottomRightFrame.place(relwidth=0.45, relheight=0.3, rely=0.3, relx=0.55)
    
    textconsole = tk.Text(root)
    textconsole.place(relwidth=0.9, relheight=0.4, rely=0.59, relx=0.05)
    textconsole["state"] = DISABLED
    fn.textconsole = textconsole

    # server = OptionMenu()
    serverlbl = ttk.Label(topLeftFrame,text="Select Web Server:",font=('Courier',13,'bold'))
    serverlbl.grid(row = 0, column = 0, sticky='ew')
    options = ["Apache", "Nginx"]
    clicked = tk.StringVar()
    clicked.set("Apache")
    serverfld = tk.OptionMenu(topLeftFrame, clicked, *options )
    serverfld.grid(row = 0, column = 1, sticky='ew')

    # logfile = Entry()
    loglbl = ttk.Label(bottomLeftFrame,text="Select Logfile Folderpath:",font=('Courier',13,'bold'))
    loglbl.grid(row = 0, column = 0)
    logfld = tk.Entry(bottomLeftFrame, text="")
    logfld.grid(row = 1, column = 0, sticky='ew')
    logBtn = tk.Button(bottomLeftFrame, text="Select directory", command=lambda:getDir(logfld))
    logBtn.grid(row = 2, column = 0, sticky='w')

    genReportBtn = tk.Button(root, text="Generate Report", command=lambda:generateReport())
    genReportBtn.place(rely=0.5, relx=0.18)

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

    genHoneyBtn = tk.Button(root, text="Generate Honeypot Pages", command=lambda:generate())
    genHoneyBtn.place(rely=0.5, relx=0.65)


    root.mainloop()