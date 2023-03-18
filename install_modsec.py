import os
import subprocess
from shutil import copyfile, rmtree

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
    copyfile(src, dest)

def create_honeypot_rules():
    honeypot_rules_path = "/etc/modsecurity/honeypot_rules.conf"
    sec_audit_log_path = "/var/log/honeypot.log"
    honeypot_rules_content = f"""# Enable ModSecurity engine
SecRuleEngine On

# Define a rule for logging request body
SecRequestBodyAccess On
SecAuditLogParts ABC
SecAuditLog {sec_audit_log_path}

# Define a location-based rule for specific pages
<Location /var/www/html/process_login.php>
   SecRule REQUEST_METHOD "POST" "id:1000,phase:1,t:none,pass,nolog,ctl:requestBodyProcessor=URLENCODED"
</Location>
<Location /var/www/html/process_search.php>
   SecRule REQUEST_METHOD "POST" "id:1000,phase:1,t:none,pass,nolog,ctl:requestBodyProcessor=URLENCODED"
</Location>
"""

    with open(honeypot_rules_path, 'w') as file:
        file.write(honeypot_rules_content)


def remove_crs_folder():
    crs_folder_path = "/etc/modsecurity/crs"
    if os.path.exists(crs_folder_path):
        rmtree(crs_folder_path)

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

def main():
    install_modsecurity()
    configure_apache2()
    copy_modsecurity_conf()
    create_honeypot_rules()
    remove_crs_folder()
    update_security2_conf()
    restart_apache2()

if __name__ == "__main__":
    main()
