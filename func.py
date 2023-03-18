# Contains the functions of generating the honeypot pages
# used by both cli.py and gui.py
import os
import shutil
from bs4 import BeautifulSoup
from tkinter.constants import DISABLED, NORMAL, END
import re
import csv

server = "Not selected"
logfile = "Not selected"
textconsole = None

def insertConsole(text):
    textconsole["state"] = NORMAL
    textconsole.insert(END, text + "\n")
    textconsole["state"] = DISABLED

# To generate the output files
def generateOutputFile(template, output, sourceFile=None):
    outputDirectory = os.path.dirname(output)
    try:
        # Check if admin login page or admin search page selected
        if "AdminLoginPageTemplate" in template:
            # Copy out javascript file and php file
            shutil.copy2("./src/login.js", outputDirectory+"/login.js")
            shutil.copy2("./src/process_login.php", outputDirectory+"/process_login.php")
        elif "SecretSearchPage" in template:
            shutil.copy2("./src/search.js", outputDirectory+"/search.js")
            shutil.copy2("./src/process_search.php", outputDirectory+"/process_search.php")
        if sourceFile:
            shutil.copy2(sourceFile, output)
        else:
            shutil.copy2(template, output)

    except IOError:
        print("(generateOutputFile) Unable to open file.")
        return None

    return output

# To extract an HTML element
def extractElement(htmlFilePath, element):
    try:
        with open(htmlFilePath, 'r', encoding='utf-8') as htmlFile:
            soup = BeautifulSoup(htmlFile.read(), 'html.parser')
            mainElement = soup.find(element)
            if mainElement:
                return str(mainElement)

    except IOError:
        print(f"Unable to open file {htmlFilePath}.")
    
    return None

# To insert a HTML element, or replace if it already exists.
def insertOrReplaceElement(outputFilePath, elementToInsertTag, afterElementTag, elementData):
    try:
        # Decode the element data
        elementData = BeautifulSoup(elementData, 'html.parser')

        # Open output file to insert element
        with open(outputFilePath, 'r+', encoding='utf-8') as outputFile:
            # Read the contents of the output file
            outputHtml = outputFile.read()

            # Create a BeautifulSoup object
            soup = BeautifulSoup(outputHtml, 'html.parser')

            # Find the element to insert after
            afterElement = soup.find(afterElementTag)

            # Find the element that to be inserted
            insertElement = soup.find(elementToInsertTag)

            # If the element to insert is not found, insert the new element after the "afterElement"
            if (not insertElement) and afterElement:
                afterElement.insert_after(elementData)
                print("Element inserted after header.")
            # If element to insert is not found and no "afterelement", insert into the body.
            elif not insertElement:
                soup.find('body').insert_after(elementData)
                print("Element inserted after body.")
            # If the element is found, replace the new element at the end of the body
            else:
                insertElement.replace_with(elementData)
                print("Element replaced.")
                
            # Write the modified HTML to the output file
            outputFile.seek(0)
            outputFile.write(str(soup))
            outputFile.truncate()

            print(f"Element '{elementToInsertTag}' added to '{outputFilePath}'")
            
    except IOError:
        print("(insertElement) Unable to open file.")

# All-in-one function to generate the honeypot pages.
def generateHoneypotPage(template, sourceFilePath, outputFile):
    try:
        # Get the current directory
        currentDir = os.getcwd()

        # Get the source template
        templateFile = os.path.join(currentDir, "templates", template)

        # Combine the current directory and the new file name to get the full path of the output file
        outputFile = os.path.join(currentDir, outputFile)

        # Generate output file first based on template file
        outputfile = generateOutputFile(templateFile, outputFile, sourceFilePath)

        if sourceFilePath != None:
            # Extract the main element from the template file
            templatemain = extractElement(templateFile, 'main')

            # Add main to output file, placed before footer if main is not present.
            insertOrReplaceElement(outputfile, "main", "header", templatemain)
        
        if template == "AdminLoginPageTemplate.html":
            print(f"The files [{os.path.basename(outputFile)}, login.js, and process_login.php] have been generated. \n\
            Please remember to edit the file name for {os.path.basename(outputFile)}.")

            insertConsole(f"The files [{os.path.basename(outputFile)}, login.js, and process_login.php] have been generated.")
            insertConsole(f"Please remember to edit the file name for {os.path.basename(outputFile)}.")

        elif template == "SecretSearchPage.html":
            print(f"The files [{os.path.basename(outputFile)}, search.js, and process_search.php] have been generated. \n\
            Please remember to edit the file name for {os.path.basename(outputFile)}.")
            
            insertConsole(f"The files [{os.path.basename(outputFile)}, search.js, and process_search.php] have been generated.")
            insertConsole(f"Please remember to edit the file name for {os.path.basename(outputFile)}.")

        # To set up logging 
        print(f"Setting up logging for {server}...")
        insertConsole(f"Setting up logging for {server}...")

        if server == "Apache":
            ApacheLoggingConfig()
        elif server == "Nginx":
            NginxLoggingConfig()

    except IOError:
        consoleReturn = "IO Exception: Unable to generate output honeypot files."
        print(consoleReturn)
        return consoleReturn

#Apache logging config
def ApacheLoggingConfig():
    # Insert logging code for apache
    print("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    insertConsole("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    
    print(f"Restarting {server} server.... Please wait")
    insertConsole(f"Restarting {server} server.... Please wait")
    # Restart Apache
    print(f"Server {server} restarted!")
    insertConsole(f"Server {server} restarted!")
    return None

def NginxLoggingConfig():
    # Insert logging code for nginx
    print("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    insertConsole("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    
    print(f"Restarting {server} server.... Please wait")
    insertConsole(f"Restarting {server} server.... Please wait")
    # Restart Nginx
    print(f"Server {server} restarted!")
    insertConsole(f"Server {server} restarted!")
    return None

# To generate report file
def parse_log_file(log_file):
    with open(log_file, 'r') as file:
        log_data = file.read()

    log_entries = re.split(r'--\w{8}-A--', log_data)[1:]
    variables_list = []

    for entry in log_entries:
        variables = entry.strip().split('\n')
        filtered_variables = [var for var in variables if not var.startswith('--') and var.strip()]

        # Split the first line into 4 sections and remove the second item
        date, unique_id, src_ip, src_port, dest_ip, dest_port = re.match(r'(\[.+\])\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)', filtered_variables[0]).groups()
        filtered_variables[0:1] = [date, f"{src_ip} {src_port}", f"{dest_ip} {dest_port}"]

        # Concatenate everything from the "--XXXXXXXX-B--" section into one cell
        concatenated_section_b = ' '.join(filtered_variables[3:])
        filtered_variables[3:] = [concatenated_section_b]

        # Get the "--XXXXXXXX-C--" section and analyze it
        section_c = re.search(r'--\w{8}-C--\s*(.+)', entry, re.DOTALL).group(1).strip()
        attack_type = analyze_attack_type(section_c)
        filtered_variables.append(attack_type)

        variables_list.append(filtered_variables)

    return variables_list

def analyze_attack_type(section_c):
    sql_keywords = ['insert', 'select', 'from', 'update', 'delete']
    xss_keywords = ['<script>', '</script>', 'alert()']

    if any(keyword.lower() in section_c.lower() for keyword in sql_keywords):
        return 'SQL Injection'
    elif any(keyword.lower() in section_c.lower() for keyword in xss_keywords):
        return 'XSS'
    else:
        return 'Unknown'

def write_to_csv(variables_list, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Add headers to the CSV file
        writer.writerow(["Timestamp", "Src IP and Port", "Dest IP and Port", "Request headers", "Type of attack"])

        for variables in variables_list:
            writer.writerow(variables)
