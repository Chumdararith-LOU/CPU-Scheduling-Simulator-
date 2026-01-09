import csv
from process import Process

def load_processes(filename):
    processes = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                p = Process(
                    pid=row['pid'],
                    arrival_time=int(row['arrival_time']),
                    burst_time=int(row['burst_time']),
                    priority=int(row['priority'])
                )
                processes.append(p)
        print(f"Successfully loaded {len(processes)} processes from {filename}")
        return processes
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except ValueError:
        print("Error: Invalid data format in CSV. Ensure numbers are integers.")
        return []

if __name__ == "__main__":
    process_list = load_processes("input.csv")
    
    print("\n--- Current Process List ---")
    for p in process_list:
        print(p)