import pyfiglet

server = ""
files = ["file1", "file2"]

def env():
    global server

    x = 1
    while (x != 0):
        print("Select the server environment on the system:")
        print("1) Nginx")
        print("2) Apache")
        print("\nSelect an option:")
        option = int(input("==> "))
        print()
        
        if option == 1:
            server = "nginx"
            print("Selected Nginx\n")
            return
        elif option == 2:
            server = "apache"
            print("Selected Apache\n")
            return


def folderpath():
    folderpath = input("State folderpath to retrieve webpages ==> ")
    print()
    getFiles(folderpath)
    return

def getFiles(folderpath):
    global files
    # Traverse folderpath to get filenames and store into "files" variable
    return

def generate():
    print("Server: " + server)
    print("Files referenced: ")
    print(files)
    print()

    print("Is the settings correct?")
    print("1) Yes")
    print("2) No")
    print("\nSelect an option:")
    option = int(input("==> "))
    print()

    if option == 1:
        genPages()
        exit(0)
    elif option == 2:
        return

def genPages():
    print("Finish generating honeypot files")
    return

if __name__ == "__main__":

    title = pyfiglet.figlet_format("Beauty On a Pot")
    print(title)
    
    x = 1
    while (x != 0):
        print("Generate the honeypot webpages by configuring the correct settings in the options:")
        print("1) Configure server environment")
        print("2) Select webpages from folderpath")
        print("3) Generate")
        print("4) Exit")
        
        print("\nSelect an option:")
        option = int(input("==> "))
        print()

        if option == 1:
            env()
        elif option == 2:
            folderpath()
        elif option == 3:
            generate() 
        elif option == 4:
            x = 0
        else:
            print("Not a valid number\n")
        
        if (x == 0):
            print("Goodbye")

         
      