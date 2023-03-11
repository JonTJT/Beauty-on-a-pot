import pyfiglet
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


def setHoneypot():
    fn.folderpath = input("Select folderpath to generate Honeypot pages ==> ")
    print()

    while (x != 0):
        print("Add/Remove generated honeypot pages: ")
        print("1) Add")
        print("2) Remove")
        print("3) Back")
        option = int(input("==> "))
        print()
        
        if option == 1:
            addPage()
        elif option == 2:
            rmPage()
        elif option == 3:
            return
        else:
            print("Invalid option")

def addPage():
    print("Add/Remove generated honeypot pages based on: ")
    print("1) Source HTML files")
    print("2) Default template")

    option = int(input("==> "))
    while (option != 1 and option != 2):
        print(option)
        print("Invalid Option")
        option = int(input("==> "))
    if (option == 1):
        source = input("Source filepath ==> ")
    elif (option == 2):
        source = "default"

    print("Type of honeypot page: ")
    print("1) Login Page")
    print("2) Search Bars")

    type = int(input("==> "))
    while (type != 1 and type != 2):
        print("Invalid Option")
        type = int(input("==> "))

    fn.generatedPages[source] = type
    return
    
def rmPage():
    i = 1
    if len(fn.generatedPages) == 0:
        print("No pages added currently")
        print()
        return
    for x in fn.generatedPages:
        print(str(i) + ") " + x)
        i += 1
    while True:
        key = input("Type the page name that is listed to remove ==> ")
        if key in fn.generatedPages:
            del fn.generatedPages[key]
            print("Succesfully deleted")
            return
        else:
            print("Incorrect key dictionary entry")

def setLogfile():
    fn.logfile = input("Select filepath to generate logs ==> ")
    print()
    return

def generate():
    x = 1
    while (x != 0):
        print("Server: " + fn.server)
        print("Output folderpath: " + fn.folderpath)
        print("Logfile path: " + fn.logfile)
        print()

        print("Is the settings correct?")
        print("1) Yes")
        print("2) No")
    
        print("\nSelect an option:")
        option = int(input("==> "))
        print()

        if option == 1:
            fn.genFiles()
            exit(0)
        elif option == 2:
            return
        else:
            print("Not a valid number!\n")


if __name__ == "__main__":
    title = pyfiglet.figlet_format("Beauty On a Pot")
    print(title)
    
    x = 1
    while (x != 0):
        print("Generate the honeypot webpages by configuring the correct settings in the options:")
        print("1) Configure server environment")
        print("2) Configure generated pages settings")
        print("3) Configure logs filepath")
        print("4) Generate")
        print("5) Exit")
        
        print("\nSelect an option:")
        option = int(input("==> "))
        print()

        if option == 1:
            setServer()
        elif option == 2:
            setHoneypot()
        elif option == 3:
            setLogfile() 
        elif option == 4:
            generate() 
        elif option == 5:
            x = 0
        else:
            print("Not a valid number\n")
        
        if (x == 0):
            print("Goodbye")

         
      