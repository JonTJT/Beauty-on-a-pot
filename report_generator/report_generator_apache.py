import os
import re
import csv

def parse_log_file(log_file):
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

    return variables_list

def analyze_attack_type(section_b, section_c):
    sql_keywords = ['insert', 'select', 'from', 'update', 'delete']
    xss_keywords = ['script', 'alert(']

    combined_sections = section_b + section_c

    if any(keyword.lower() in combined_sections.lower() for keyword in sql_keywords):
        return 'SQL Injection'
    elif any(keyword.lower() in combined_sections.lower() for keyword in xss_keywords):
        return 'XSS'
    else:
        return 'Unknown'

def write_to_csv(variables_list, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Src IP and Port", "Dest IP and Port", "Request headers", "Type of attack"])

        for variables in variables_list:
            writer.writerow(variables)

def main():
    log_file = './logs/apache_test2.log'
    csv_file = './reports/test_csv.csv'

    if not os.path.isfile(log_file):
        print(f"{log_file} not found.")
        return

    variables_list = parse_log_file(log_file)
    write_to_csv(variables_list, csv_file)
    print(f"Data successfully written to {csv_file}")

if __name__ == '__main__':
    main()
