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
        option = int(input("==> "))
        print()
        
        if option == 1:
            fn.server = "Nginx"
            print("Selected Nginx\n")
            return
        elif option == 2:
            fn.server = "Apache"
            print("Selected Apache\n")
            return

def addPage():
    print("Type of honeypot page: ")
    print("1) Login Page")
    print("2) Search Bar")
    type = int(input("==> "))
    print()
    while (type != 1 and type != 2):
        print("Invalid Option")
        type = int(input("==> "))
        print()
    if type == 1:
        template = "AdminLoginPageTemplate.html"
    elif type == 2:
        template = "SecretSearchPage.html"

    print("From Source/Default:")
    print("1) Source HTML files")
    print("2) Default template")
    srcOption = int(input("==> "))
    print()
    while (srcOption != 1 and srcOption != 2):
        print("Invalid Option")
        srcOption = int(input("==> "))
        print()
    if srcOption == 1:
        source = input("Source filepath ==> ")
        print()
    elif srcOption == 2:
        source = None

    root_ext = ""
    if source == None:
        root_ext = os.path.splitext("default.html")
    else:
        root_ext = os.path.splitext(source)

    if type == 1:
        outputFile = root_ext[0] + "_AdminLoginHoneypot" + root_ext[1]
    if type == 2:
        outputFile = root_ext[0] + "_SearchHoneypot" + root_ext[1]

    fn.generateHoneypotPage(template, source, outputFile)
    return


def setLogfile():
    fn.logfile = input("Select filepath to generate logs ==> ")
    print()
    return

def generate():
    # fn.folderpath = input("Select folderpath to generate Honeypot pages ==> ")
    while(True):
        print("1) Generate a honeypot page")
        print("2) Finish")
        option = int(input("==> "))
        print()

        if option == 1:
            addPage()
        elif option == 2:
            return
        else:
            print("Not a valid number!\n")

if __name__ == "__main__":
    title = pyfiglet.figlet_format("Beauty On a Pot")
    print(title)
    
    x = 1
    while (x != 0):
        print("Selected web server environment: " + fn.server)
        print("Selected log filepath: " + fn.logfile)
        print("Generate the honeypot webpages by configuring the correct settings in the options:")
        print("1) Specify server environment")
        print("2) Specify logs filepath")
        print("3) Generate Honeypot Pages")
        print("4) Exit")
        
        print("\nSelect an option:")
        option = int(input("==> "))
        print()

        if option == 1:
            setServer()
        elif option == 2:
            setLogfile() 
        elif option == 3:
            generate()
            x = 0
        elif option == 4:
            x = 0
        else:
            print("Not a valid number\n")
        
        if (x == 0):
            print("Goodbye")

         
      