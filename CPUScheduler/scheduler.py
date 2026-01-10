from collections import deque


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


def solve_rr(processes, quantum):
    print(f"--- Running Round Robin Algorithm (Quantum={quantum}) ---")
    
    # Sort by arrival first to easily manage initial loading
    processes.sort(key=lambda p: p.arrival_time)
    
    n = len(processes)
    queue = deque()
    current_time = 0
    completed = 0
    gantt_data = [] 
    
    in_queue_indices = set()
    
    # Helper to push new arrivals to queue
    def check_new_arrivals(time):
        for i, p in enumerate(processes):
            if p.arrival_time <= time and i not in in_queue_indices and p.remaining_time > 0:
                queue.append(i)
                in_queue_indices.add(i)

    # Initial load
    check_new_arrivals(current_time)
    
    while completed < n:
        if not queue:
            # Idle time logic
            current_time += 1
            check_new_arrivals(current_time)
            continue
            
        # Get next process index
        idx = queue.popleft()
        p = processes[idx]
        
        # Determine run time (Process runs for Quantum OR until completion)
        run_time = min(quantum, p.remaining_time)
        
        # Metrics: Response Time (First time it runs)
        if p.start_time == -1:
            p.start_time = current_time
            
        # Record execution for Gantt
        gantt_data.append((p.pid, current_time, current_time + run_time))
        
        # Execute
        p.remaining_time -= run_time
        current_time += run_time
        
        check_new_arrivals(current_time)
        
        # Completion Check
        if p.remaining_time == 0:
            completed += 1
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.response_time = p.start_time - p.arrival_time
        else:
            # Not finished? Back to the queue
            queue.append(idx)
            
    return processes, gantt_data

def solve_mlfq(processes, aging_interval=20):
    print(f"--- Running MLFQ Algorithm (Aging Interval={aging_interval}) ---")
    
    # Sort for easier arrival checks
    processes.sort(key=lambda p: p.arrival_time)
    
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_data = []
    
    # 3 Levels of Queues
    # queue_level 0 = RR(Q=2)
    # queue_level 1 = RR(Q=4)
    # queue_level 2 = FCFS
    queues = [deque(), deque(), deque()]
    quantums = [2, 4, float('inf')]
    
    # Track dynamic state
    # We need to map PID to which queue level it is currently in
    p_level = {p.pid: 0 for p in processes}
    
    # We also need to track how much time the current process has burned in its CURRENT quantum
    current_proc = None
    time_slice = 0
    
    last_pid = None
    start_time_block = 0
    
    while completed < n:
        # 1. Check for New Arrivals
        # Important: Add them to Q0 (High Priority)
        for p in processes:
            if p.arrival_time == current_time:
                queues[0].append(p)
                p_level[p.pid] = 0
        
        # 2. Check Aging (Prevent Starvation)
        # Every 'aging_interval' units, reset everyone to Q0
        if current_time > 0 and current_time % aging_interval == 0:
            # Move everyone from Q1 and Q2 back to Q0
            for q_idx in range(1, 3):
                while queues[q_idx]:
                    proc = queues[q_idx].popleft()
                    queues[0].append(proc)
                    p_level[proc.pid] = 0
                    # Note: In a real OS, we might handle running processes differently,
                    # but here we just shuffle the waiting ones.
        
        # 3. Select Process to Run (Highest Priority Non-Empty Queue)
        active_queue_index = -1
        if queues[0]: active_queue_index = 0
        elif queues[1]: active_queue_index = 1
        elif queues[2]: active_queue_index = 2
        
        # PREEMPTION CHECK:
        # If we were running a process from a lower queue (e.g. Q2), 
        # and something just arrived in Q0, we must stop the Q2 process.
        if current_proc and p_level[current_proc.pid] > active_queue_index and active_queue_index != -1:
            # Put current process back to the FRONT (or end) of its own queue level?
            # Standard RR usually puts it at the tail.
            queues[p_level[current_proc.pid]].append(current_proc)
            current_proc = None
            time_slice = 0

        # If no process is running, pick one
        if not current_proc and active_queue_index != -1:
            current_proc = queues[active_queue_index].popleft()
            time_slice = 0
            
        # 4. Update Gantt (Visualization Logic)
        if current_proc:
            if current_proc.pid != last_pid:
                if last_pid is not None:
                    gantt_data.append((last_pid, start_time_block, current_time))
                last_pid = current_proc.pid
                start_time_block = current_time
            
            # Metric: Response Time
            if current_proc.start_time == -1:
                current_proc.start_time = current_time
                
            # EXECUTE
            current_proc.remaining_time -= 1
            time_slice += 1
            current_time += 1
            
            # Check Completion
            if current_proc.remaining_time == 0:
                completed += 1
                current_proc.completion_time = current_time
                current_proc.turnaround_time = current_proc.completion_time - current_proc.arrival_time
                current_proc.waiting_time = current_proc.turnaround_time - current_proc.burst_time
                current_proc.response_time = current_proc.start_time - current_proc.arrival_time
                current_proc = None # CPU is free
                time_slice = 0
            
            # Check Quantum Expiration (Demotion)
            elif time_slice >= quantums[p_level[current_proc.pid]]:
                # Demote to next level (max level is 2)
                next_level = min(2, p_level[current_proc.pid] + 1)
                p_level[current_proc.pid] = next_level
                queues[next_level].append(current_proc)
                current_proc = None # CPU is free
                time_slice = 0
                
        else:
            # IDLE
            if last_pid is not None:
                gantt_data.append((last_pid, start_time_block, current_time))
                last_pid = None
            
            current_time += 1
            start_time_block = current_time

    # Final Gantt flush
    if last_pid is not None:
        gantt_data.append((last_pid, start_time_block, current_time))
        
    return processes, gantt_data