import csv
import os

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

def generate_nginx_report():
    input_file = "logs/nginxhoneypot.log"
    output_file = "reports/nginx_output.csv"

    if not os.path.isfile(input_file):
        print("Input file missing. Exiting.")
        exit()

    with open(input_file, 'r') as f:
        logs = f.read().split('|')

        with open(output_file, 'w+', newline='') as csvfile:
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


generate_nginx_report()