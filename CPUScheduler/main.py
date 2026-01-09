import csv
from process import Process
from scheduler import solve_fcfs

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
    
def print_results(processes, gantt):
    print("\nPID\tArrival\tBurst\tFinish\tWait\tTurnaround\tResponse")
    print("-" * 65)
    
    total_wait = 0
    total_turnaround = 0
    total_response = 0
    
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t"
              f"{p.waiting_time}\t{p.turnaround_time}\t\t{p.response_time}")
        
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time
        
    n = len(processes)
    print("-" * 65)
    print(f"Averages:\t\t\t{total_wait/n:.2f}\t{total_turnaround/n:.2f}\t\t{total_response/n:.2f}")

if __name__ == "__main__":
    process_list = load_processes("input.csv")
    
    if process_list:
        fcfs_result, fcfs_gantt = solve_fcfs(process_list[:])
        
        print_results(fcfs_result, fcfs_gantt)