class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid                   
        self.arrival_time = arrival_time 
        self.burst_time = burst_time     
        self.priority = priority         
        
        self.remaining_time = burst_time 
        
        self.start_time = -1            
        self.completion_time = 0        
        self.waiting_time = 0            
        self.turnaround_time = 0        
        self.response_time = 0          

    def __repr__(self):
        return f"Process({self.pid}, Arrival={self.arrival_time}, Burst={self.burst_time})"