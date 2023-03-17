# log_parser.py
import os
import csv

def parse_log_file(log_file):
    with open(log_file, 'r') as file:
        log_data = file.read()

    log_entries = log_data.split('|')

    variables_list = []
    for entry in log_entries:
        variables = entry.strip().split('\n')
        variables_list.append(variables)

    return variables_list

def write_to_csv(variables_list, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for variables in variables_list:
            writer.writerow(variables)

def main():
    log_file = 'test_log.log'
    csv_file = 'test_csv.csv'

    if not os.path.isfile(log_file):
        print(f"{log_file} not found.")
        return

    variables_list = parse_log_file(log_file)
    write_to_csv(variables_list, csv_file)
    print(f"Data successfully written to {csv_file}")

if __name__ == '__main__':
    main()
