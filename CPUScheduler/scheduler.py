def solve_fcfs(processes):
    print("--- Running FCFS Algorithm ---")
    
    processes.sort(key=lambda p: p.arrival_time)
    
    current_time = 0
    gantt_data = [] 
    
    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
            
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.start_time - p.arrival_time
        
        gantt_data.append((p.pid, p.start_time, p.completion_time))
        
        current_time = p.completion_time
        
    return processes, gantt_data


def solve_sjf(processes):
    print("--- Running SJF Algorithm (Non-Preemptive) ---")
    
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_data = []
    

    is_completed = [False] * n
    
    while completed < n:
        ready_queue = []
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                ready_queue.append(i) 
        
        if not ready_queue:
            next_arrival = float('inf')
            for p in processes:
                if p.arrival_time > current_time:
                    next_arrival = min(next_arrival, p.arrival_time)
            current_time = next_arrival
            continue

        idx_to_run = min(ready_queue, key=lambda i: processes[i].burst_time)
        p = processes[idx_to_run]
        
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.start_time - p.arrival_time
        
        gantt_data.append((p.pid, p.start_time, p.completion_time))
        
        is_completed[idx_to_run] = True
        completed += 1
        current_time = p.completion_time
        
    return processes, gantt_data


def solve_srt(processes):
    print("--- Running SRT Algorithm (Preemptive) ---")
    
    # Sort by arrival time initially to handle the queue easier visually
    processes.sort(key=lambda p: p.arrival_time)
    
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_data = [] # Store (PID, start, end)
    
    # To detect context switches for the Gantt chart
    last_pid = None
    start_time_block = 0
    
    while completed < n:
        # 1. Find all available processes that are NOT done
        ready_queue = []
        for p in processes:
            if p.arrival_time <= current_time and p.remaining_time > 0:
                ready_queue.append(p)
        
        if not ready_queue:
            if last_pid is not None:
                gantt_data.append((last_pid, start_time_block, current_time))
                last_pid = None
            
            current_time += 1
            start_time_block = current_time # Reset block start
            continue

        current_process = min(ready_queue, key=lambda p: (p.remaining_time, p.arrival_time))
        
        if current_process.start_time == -1:
            current_process.start_time = current_time
            
        if current_process.pid != last_pid:
            if last_pid is not None:
                 gantt_data.append((last_pid, start_time_block, current_time))
            last_pid = current_process.pid
            start_time_block = current_time
            
        current_process.remaining_time -= 1
        current_time += 1
        
        if current_process.remaining_time == 0:
            completed += 1
            current_process.completion_time = current_time
            
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            current_process.response_time = current_process.start_time - current_process.arrival_time

    if last_pid is not None:
        gantt_data.append((last_pid, start_time_block, current_time))
        
    return processes, gantt_data