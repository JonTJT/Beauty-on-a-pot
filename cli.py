import pyfiglet
import os
import func as fn

def setServer():
    x = 1
    while (x != 0):
        print("Select the server environment on the system:")
        print("1) Nginx")
        print("2) Apache")
        print("\nSelect an option:")
        option = input("==> ")
        print()
        
        if option == '1':
            fn.server = "Nginx"
            print("Selected Nginx\n")
            return
        elif option == '2':
            fn.server = "Apache"
            print("Selected Apache\n")
            return
        else:
            print("ERROR: Invalid option.\n")

def addPage():
    while True:
        print("Type of honeypot page: ")
        print("1) Login Page")
        print("2) Search Bar")
        print()
        type = input("==> ")
        print()
        if (type == '1') or (type == '2'):
            break
        else:
            print("ERROR: Invalid option.\n")
    if type == '1':
        template = "AdminLoginPageTemplate.html"
    elif type == '2':
        template = "SecretSearchPage.html"

    source = None
    while (True):
        print("From Source/Default:")
        print("1) Source HTML files")
        print("2) Default template")
        srcOption = input("==> ")
        if srcOption == '1':
            source = input("Source filepath ==> ")
            print()
            if not os.path.isfile(source):
                print("ERROR: File is invalid. Please enter in the full file path of the source file.\n")
            else:
                break
        elif srcOption == '2':
            break
        else:
            print("ERROR: Invalid Option\n")

    root_ext = ""
    if source == None:
        root_ext = os.path.splitext("default.html")
    else:
        root_ext = os.path.splitext(source)

    if type == '1':
        outputFile = root_ext[0] + "_AdminLoginHoneypot" + root_ext[1]
    if type == '2':
        outputFile = root_ext[0] + "_SearchHoneypot" + root_ext[1]

    # Generate honeypot pages
    fn.generateHoneypotPage(template, source, outputFile)

    # Set up logging & restart server
    return

def setLogFolder():
    try:
        while True:
            logfile = input("Select folder to store log file ==> ")
            print()
        
            if os.path.exists(logfile):
                fn.logfile = logfile
                break
            else:
                print("ERROR: Directory does not exist or is invalid.\n")
    except:
        print("ERROR: Unable to set log file path.\n")
    return

def GenerateHoneypotPages():
    while(True):
        print("1) Generate a honeypot page")
        print("2) Finish")
        option = input("==> ")
        print()

        if option == '1':
            addPage()
            break
        elif option == '2':
            return
        else:
            print("ERROR: Invalid Option\n")

def GenerateReport(logFile):
    logFilePath = logFile + "/honeypot.log"
    try:
        if fn.server == "Apache":
            fn.ApacheGenerateReport(logFilePath)
        elif fn.server == "Nginx":
            fn.NginxGenerateReport(logFilePath)
    except:
        print("An error has occured, unable to generate report file.")

if __name__ == "__main__":
    title = pyfiglet.figlet_format("Beauty On a Pot")
    print(title)

    while True:
        print("Selected web server environment: " + fn.server)
        print("Selected log file directory: " + fn.logfile)
        print("Generate the honeypot webpages by configuring the correct settings in the options:")
        print("1) Specify server environment")
        print("2) Specify logs filepath")
        print("3) Generate Honeypot Pages")
        print("4) Generate Report")
        print("5) Exit")
        
        print("\nSelect an option:")
        option = input("==> ")
        print()

        if option == '1':
            setServer()
        elif option == '2':
            setLogFolder()
        elif option == '3':
            # Ensure both logfile and server are selected.
            if (fn.logfile != "Not selected") and (fn.server != "Not selected"):
                GenerateHoneypotPages()
            else:
                print("ERROR: Web server / Log file not selected. Please ensure both are selected.\n")
        elif option == '4':
            # Check if web serer & log file path is selected
            if (fn.server == "Not selected") or (fn.logfile == "Not selected"):
                print("ERROR: Web server / Log file not selected. Please ensure both are selected.\n")
                continue
            GenerateReport(fn.logfile)

        elif option == '5':
            break
        else:
            print("ERROR: Not a valid option, please enter a number between 1 and 5.\n")

    print("Goodbye")

         
      