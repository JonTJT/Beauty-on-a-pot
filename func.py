# Contains the functions of generating the honeypot pages
# used by both cli.py and gui.py

server = ""
folderpath = ""
logfile = ""
    
def genFiles():
    # Generate html files
    filepath1 = folderpath + "/test.txt"
    filepath2 = folderpath + "/test.txt"

    with open(filepath1, 'w') as f:
        f.write('Hello World!')

    print("Finish generating honeypot files")
    return