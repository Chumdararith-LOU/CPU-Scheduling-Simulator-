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