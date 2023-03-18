# Contains the functions of generating the honeypot pages
# used by both cli.py and gui.py
import os
import shutil
from bs4 import BeautifulSoup
from tkinter.constants import DISABLED, NORMAL, END
import re
import csv
import subprocess
import time

server = "Not selected"
logfile = "Not selected"
textconsole = None

def insertConsole(text):
    if textconsole != None:
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

    except Exception as e:
        consoleReturn = f"ERROR: An error has occured. {e}\n"
        print(consoleReturn)
        insertConsole(consoleReturn)

# To extract an HTML element
def extractElement(htmlFilePath, element):
    try:
        with open(htmlFilePath, 'r', encoding='utf-8') as htmlFile:
            soup = BeautifulSoup(htmlFile.read(), 'html.parser')
            mainElement = soup.find(element)
            if mainElement:
                return str(mainElement)

    except Exception as e:
        consoleReturn = f"ERROR: An error has occured while extracting HTML element. {e}\n"
        print(consoleReturn)
        insertConsole(consoleReturn)
    
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
            
    except Exception as e:
        consoleReturn = f"ERROR: An error has occured with trying to insert/replace HTML element. {e}\n"
        print(consoleReturn)
        insertConsole(consoleReturn)

# All-in-one function to generate the honeypot pages.
def generateHoneypotPage(template, sourceFilePath, outputFile):
    try:
        # Get the current directory
        currentDir = os.getcwd()

        # Get the source template
        templateFile = os.path.join(currentDir, "templates", template)

        # Generate output file first based on template file
        generateOutputFile(templateFile, outputFile, sourceFilePath)

        if sourceFilePath != None:
            # Extract the main element from the template file
            templatemain = extractElement(templateFile, 'main')

            # Add main to output file, placed before footer if main is not present.
            insertOrReplaceElement(outputFile, "main", "header", templatemain)
        
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

    except Exception as e:
        consoleReturn = f"ERROR: An error has occured with the honeypot page generation process. {e}\n"
        print(consoleReturn)
        insertConsole(consoleReturn)

    try:
        # To set up logging 
        print(f"Setting up logging for {server}...")
        insertConsole(f"Setting up logging for {server}...")

        if server == "Apache":
            apache_log_setup(logfile)
        elif server == "Nginx":
            nginx_log_setup(logfile)

    except Exception as e:
        consoleReturn = f"ERROR: An error has occured with the logging installation process. {e}\n"
        print(consoleReturn)
        insertConsole(consoleReturn)

# To generate report file for Apache
def ApacheLogParser(log_file, csv_file):
    with open(log_file, 'r') as file:
        log_data = file.read()

    log_entries = re.split(r'--\w{8}-A--', log_data)[1:]
    variables_list = []

    for entry in log_entries:
        variables = entry.strip().split('\n')
        filtered_variables = [var for var in variables if not var.startswith('--') and var.strip()]

        date, unique_id, src_ip, src_port, dest_ip, dest_port = re.match(r'(\[.+\])\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)', filtered_variables[0]).groups()
        filtered_variables[0:1] = [date, f"{src_ip} {src_port}", f"{dest_ip} {dest_port}"]

        concatenated_section_b = ' '.join(filtered_variables[3:])
        filtered_variables[3:] = [concatenated_section_b]

        section_c_search = re.search(r'--\w{8}-C--\s*(.+)', entry, re.DOTALL)
        section_c = section_c_search.group(1).strip() if section_c_search else ''

        attack_type = analyze_attack_type(concatenated_section_b, section_c)
        filtered_variables.append(attack_type)

        variables_list.append(filtered_variables)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Src IP and Port", "Dest IP and Port", "Request headers", "Type of attack"])

        for variables in variables_list:
            writer.writerow(variables)

def analyze_attack_type(section_b, section_c):
    sql_keywords = ['insert', 'select', 'from', 'update', 'delete']
    xss_keywords = ['script', 'alert(', 'prompt(']

    combined_sections = section_b + section_c

    if any(keyword.lower() in combined_sections.lower() for keyword in sql_keywords):
        return 'SQL Injection'
    elif any(keyword.lower() in combined_sections.lower() for keyword in xss_keywords):
        return 'XSS'
    else:
        return 'Unknown'

# To generate report file for Apache
def ApacheGenerateReport(logFile):
    # Generate report file if not present
    if not os.path.exists('./reports'):
        os.makedirs('./reports')
    CSVfile = "./reports/" + str(int(time.time())) + ".csv"

    try:
        if not os.path.isfile(logFile):
            print(f"ERROR: {logFile} not found.\n")
            insertConsole(f"ERROR: {logFile} not found.\n")
            return

        ApacheLogParser(logFile, CSVfile)
        print(f"Data successfully written to {CSVfile}")
        insertConsole(f"Data successfully written to {CSVfile}")

    except Exception as e:
        print(f"ERROR: Unable to generate report. {e}\n")
        insertConsole(f"ERROR: Unable to generate report.{e}\n")        

# To generate report file for nginx
def NginxGenerateReport(logFile):
    # Generate report file if not present
    if not os.path.exists('./reports'):
        os.makedirs('./reports')
    CSVfile = "./reports/" + str(int(time.time())) + ".csv"

    if not os.path.isfile(logFile):
        print(f"ERROR: {logFile} not found.\n")
        insertConsole(f"ERROR: {logFile} not found.\n")
        return

    try:
        with open(logFile, 'r') as f:
            logs = f.read().split('|')

            with open(CSVfile, 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Src IP and Port", "Dest IP and Port", "Request headers", "Type of attack"])

                for log in logs:

                    log = log.strip('\n')
                    if log == "":
                        continue

                    log_lines = log.split('\n')
                    timestamp_src_dst = log_lines[0].split(" ")
                    timestamp = timestamp_src_dst[0] + " " + timestamp_src_dst[1]
                    src = timestamp_src_dst[2] + " " + timestamp_src_dst[3]
                    dst = timestamp_src_dst[4] + " " + timestamp_src_dst[5]
                    headers_body = ' '.join(log_lines[1:])
                    attack_type = analyze_attack_type(headers_body, "")

                    writer.writerow([timestamp, src, dst, headers_body, attack_type])
    except Exception as e:
        print(f"ERROR: Unable to generate report. {e}\n")
        insertConsole(f"ERROR: Unable to generate report.{e}\n")        

# For APACHE Log installation
def install_modsecurity():
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libapache2-mod-security2'])

def configure_apache2():
    apache2_conf_path = "/etc/apache2/apache2.conf"
    lines_to_add = [
        "LoadModule security2_module /usr/lib/apache2/modules/mod_security2.so",
        "IncludeOptional /etc/modsecurity/honeypot_rules.conf"
    ]

    with open(apache2_conf_path, 'r') as file:
        apache2_conf = file.readlines()

    for line in lines_to_add:
        if not any(line in conf_line for conf_line in apache2_conf):
            with open(apache2_conf_path, 'a') as file:
                file.write(f"{line}\n")

def copy_modsecurity_conf():
    src = "/etc/modsecurity/modsecurity.conf-recommended"
    dest = "/etc/modsecurity/modsecurity.conf"
    shutil.copyfile(src, dest)

def has_existing_apache_configuration(file_path, unique_strings, sec_audit_log_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist. Skipping the configuration check.")
        return False

    sec_audit_log_line_found = False
    for unique_string in unique_strings:
        if unique_string != "SecAuditLog":
            if any(unique_string in line for line in lines):
                return True
        else:
            for line in lines:
                if "SecAuditLog" in line:
                    sec_audit_log_line_found = True
                    if sec_audit_log_path in line:
                        return True

    return sec_audit_log_line_found and any("SecAuditLog" in line for line in lines)



def create_honeypot_rules(sec_audit_log_path):
    honeypot_rules_path = "/etc/modsecurity/honeypot_rules.conf"
    sec_audit_log_path = sec_audit_log_path + "/honeypot.log"
    honeypot_rules_content = f"""# Enable ModSecurity engine
SecRuleEngine On

# Define a rule for logging request body
SecRequestBodyAccess On
SecAuditLogParts ABC
SecAuditLog {sec_audit_log_path}

# Define a location-based rule for specific pages
<Location {os.getcwd() + '/process_login.php'}>
   SecRule REQUEST_METHOD "POST" "id:1000,phase:1,t:none,pass,nolog,ctl:requestBodyProcessor=URLENCODED"
</Location>
<Location {os.getcwd() + '/process_search.php'}>
   SecRule REQUEST_METHOD "POST" "id:1000,phase:1,t:none,pass,nolog,ctl:requestBodyProcessor=URLENCODED"
</Location>
"""

    unique_strings = [
        "SecRuleEngine On",
        "SecRequestBodyAccess On",
        "SecAuditLogParts ABC",
        "SecAuditLog"
    ]

    if has_existing_apache_configuration(honeypot_rules_path, unique_strings, sec_audit_log_path + "/honeypot.log"):
        print("The honeypot_rules.conf file has already been modified with the same log path. Skipping the configuration process.")
        return

    with open(honeypot_rules_path, 'w') as file:
        file.write(honeypot_rules_content)

# (rest of the code remains the same)


def remove_crs_folder():
    crs_folder_path = "/etc/modsecurity/crs"
    if os.path.exists(crs_folder_path):
        shutil.rmtree(crs_folder_path)

def update_security2_conf():
    security2_conf_path = "/etc/apache2/mods-enabled/security2.conf"
    lines_to_remove = [
        "# Include OWASP ModSecurity CRS rules if installed",
        "IncludeOptional /usr/share/modsecurity-crs/*.load"
    ]

    with open(security2_conf_path, 'r') as file:
        security2_conf = file.readlines()

    with open(security2_conf_path, 'w') as file:
        for line in security2_conf:
            if line.strip() not in lines_to_remove:
                file.write(line)

def restart_apache2():
    subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'])

def apache_log_setup(log_path):
    # Insert logging code for apache
    
    install_modsecurity()
    configure_apache2()
    copy_modsecurity_conf()
    create_honeypot_rules(log_path)
    remove_crs_folder()
    update_security2_conf()
    print(f"Logging successfully configured. Logging file path has been set to: {log_path + '/honeypot.log'}")
    insertConsole(f"Logging successfully configured. Logging file path has been set to: {log_path + '/honeypot.log'}")

    print(f"Restarting {server} server.... Please wait")
    insertConsole(f"Restarting {server} server.... Please wait")

    restart_apache2()

    print(f"Server {server} restarted!")
    insertConsole(f"Server {server} restarted!")
    return None

# For NGINX Log installation

def has_existing_nginx_configuration(lines):
    unique_strings = [
        "log_format log_req",
        "lua_need_request_body on;",
        "location = /process_login.php",
        "location = /process_search.php"
    ]

    for unique_string in unique_strings:
        if any(unique_string in line for line in lines):
            return True

    return False

def nginx_log_setup(log_path):
    # Set expected php path to check for
    PHP_DIR = '/etc/php/8.2/fpm'

    # Set the path to the Nginx config file
    CONFIG_FILE = os.getcwd() + "/../conf/nginx.conf"
    CONFIG_FILE = '/usr/local/openresty/nginx/conf/nginx.conf'

    # Define the string to insert for log_format
    LOG_FORMAT_STRING = '''    log_format log_req escape=none '[$time_local] $remote_addr $remote_port $server_addr $server_port'\n    '\\n$request$req_header$request_body\\n|\\n';\n\n'''

    # Define the  string to insert for lua processing
    LUA_STRING = f'''
        lua_need_request_body on;

        set $req_header "\\n";
        header_filter_by_lua_block {{
        local h = ngx.req.get_headers()
        for k, v in pairs(h) do
                if (type(v) == "table") then
                ngx.var.req_header = ngx.var.req_header .. k.."="..table.concat(v,",").."\\n"
                else
                ngx.var.req_header = ngx.var.req_header .. k.."="..v.."\\n"
                end
        end
        }}\n\n'''

    # Define the string to insert for location
    LOCATION_STRING = f'''
        location = /process_login.php {{
            fastcgi_pass unix:/run/php/php8.2-fpm.sock;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;

            access_log {log_path + '/honeypot.log'} log_req;
        }}

        location = /process_search.php {{
            fastcgi_pass unix:/run/php/php8.2-fpm.sock;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;

            access_log {log_path + '/honeypot.log'} log_req;
        }}
    '''

    # Check if php version is correct
    if not os.path.isdir(PHP_DIR):
        print('Please confirm if php8.2 is installed. If the version of php used is not 8.2, please edit this script to reflect the correct version.')
        exit(0)

    # Create a backup nginx.conf file
    if not os.path.isfile('/usr/local/openresty/nginx/conf/nginx.conf.backup'):
        os.system('cp /usr/local/openresty/nginx/conf/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf.backup')
        print('Backup created as /usr/local/openresty/nginx/conf/nginx.conf.backup.')

     # Use awk to find the http block and insert the strings
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()

    if has_existing_nginx_configuration(lines):
        print("The configuration file has already been modified. Skipping the configuration process.")
        return

    with open(CONFIG_FILE + '.tmp', 'w') as f:
        in_http_block = False
        in_server_block = False
        in_location_block = False
        http_write = False
        server_write = False
        location_write = False
        for line in lines:
            if 'http {' in line and not http_write:
                in_http_block = True
                http_write = True
                f.write(line)
                f.write(LOG_FORMAT_STRING)
            elif 'server {' in line and not server_write:
                in_server_block = True
                server_write = True
                f.write(line)
                f.write(LUA_STRING)
            elif 'location /' in line:
                in_location_block = True
                f.write(line)
            elif in_location_block and '}' in line and not location_write:
                in_location_block = False
                f.write(line)
                f.write(LOCATION_STRING)
                location_write = True
            # elif in_http_block or in_server_block or in_location_block:
            #     pass
            else:
                f.write(line)

    # Overwrite the original config file with the modified version
    os.system('mv ' + CONFIG_FILE + '.tmp ' + CONFIG_FILE)

    print("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    insertConsole("Logging successfully configured. Logging file path has been set to: '/var/log/honeypot.log'")
    
    print(f"Restarting {server} server.... Please wait")
    insertConsole(f"Restarting {server} server.... Please wait")

    subprocess.run(['sudo', 'systemctl', 'restart', 'openresty'])
    
    # Restart Nginx
    print(f"Server {server} restarted!")
    insertConsole(f"Server {server} restarted!")