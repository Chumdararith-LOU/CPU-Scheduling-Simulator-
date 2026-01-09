import csv
import os
from process import Process
from scheduler import solve_fcfs, solve_sjf, solve_srt, solve_rr, solve_mlfq

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
    
def print_gantt_chart(gantt_data):
    print("\n--- Gantt Chart ---")
    # gantt_data is a list of tuples: (PID, Start, End)
    
    # Top border
    print(" ", end="")
    for entry in gantt_data:
        pid, start, end = entry
        duration = end - start
        print("-" * duration * 2 + " ", end="") # scale width by 2 for visibility
    print()
    
    # PID Row
    print("|", end="")
    for entry in gantt_data:
        pid, start, end = entry
        duration = end - start
        # Center the PID in the block
        fmt = f"{{:^{duration*2}}}"
        print(fmt.format(pid) + "|", end="")
    print()
    
    # Bottom border
    print(" ", end="")
    for entry in gantt_data:
        pid, start, end = entry
        duration = end - start
        print("-" * duration * 2 + " ", end="")
    print()
    
    # Timeline
    print("0", end="")
    for entry in gantt_data:
        pid, start, end = entry
        duration = end - start
        fmt = f"{{:>{duration*2}}}"
        print(fmt.format(end) + " ", end="") # Simple timeline
    print("\n")

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
    print_gantt_chart(gantt)

def export_to_csv(filename, processes, algorithm_name):
    """
    Saves the processing metrics to a CSV file.
    """
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write Header
            writer.writerow(["Algorithm", algorithm_name])
            writer.writerow([]) # Empty line
            writer.writerow(["PID", "Arrival", "Burst", "Finish", "Wait", "Turnaround", "Response"])
            
            # Write Data
            total_wait = 0
            total_turnaround = 0
            total_response = 0
            n = len(processes)
            
            for p in processes:
                writer.writerow([
                    p.pid, 
                    p.arrival_time, 
                    p.burst_time, 
                    p.completion_time, 
                    p.waiting_time, 
                    p.turnaround_time, 
                    p.response_time
                ])
                total_wait += p.waiting_time
                total_turnaround += p.turnaround_time
                total_response += p.response_time
            
            # Write Averages
            writer.writerow([])
            writer.writerow(["Averages", "", "", "", 
                             f"{total_wait/n:.2f}", 
                             f"{total_turnaround/n:.2f}", 
                             f"{total_response/n:.2f}"])
            
        print(f"✅ Results exported to '{filename}'")
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")

if __name__ == "__main__":
    process_list = load_processes("input.csv")

    output_dir = "output_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if process_list:
        # Run FCFS
        print("\n" + "="*30)
        fcfs_result, fcfs_gantt = solve_fcfs(process_list[:])
        
        print_results(fcfs_result, fcfs_gantt)

        # Run SJF
        print("\n" + "="*30)
        process_list_sjf = load_processes("input.csv") 
        sjf_result, sjf_gantt = solve_sjf(process_list_sjf)
        print_results(sjf_result, sjf_gantt)

        # Run SRT
        print("\n" + "="*30)
        process_list_srt = load_processes("input.csv") 
        srt_result, srt_gantt = solve_srt(process_list_srt)
        print_results(srt_result, srt_gantt)

        # Run RR
        print("\n" + "="*30)
        process_list_rr = load_processes("input.csv") 
        # Note: The requirement says Quantum = 2 for the sample scenario
        rr_result, rr_gantt = solve_rr(process_list_rr, quantum=2)
        print_results(rr_result, rr_gantt)

        # Run MLFQ
        print("\n" + "="*30)
        process_list_mlfq = load_processes("input.csv") 
        # Using a large aging interval (e.g. 20) to see normal behavior first
        mlfq_result, mlfq_gantt = solve_mlfq(process_list_mlfq, aging_interval=20)
        print_results(mlfq_result, mlfq_gantt)