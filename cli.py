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


def setFolderpath():
    fn.folderpath = input("Select folderpath to generate Honeypot pages ==> ")
    print()
    return

def setLogfile():
    fn.logfile = input("Select filepath to generate logs ==> ")
    print()
    return

def generate():
    x = 1
    while (x != 0):
        print("Server: " + fn.server)
        print("Folderpath: " + fn.folderpath)
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
        print("2) Configure folderpath for honeypot pages")
        print("3) Configure filepath for log files")
        print("4) Generate")
        print("5) Exit")
        
        print("\nSelect an option:")
        option = int(input("==> "))
        print()

        if option == 1:
            setServer()
        elif option == 2:
            setFolderpath()
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

         
      