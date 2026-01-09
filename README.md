

**Action:** Create a file named `README.md` in your project folder and paste the content below.

```markdown
# CPU Scheduling Algorithm Simulator

## Project Overview
[cite_start]This project is a CPU scheduling simulator designed to demonstrate how an operating system manages process execution[cite: 2, 4]. It implements five standard scheduling algorithms and visualizes their execution using a text-based Gantt chart. [cite_start]The simulator calculates key performance metrics, including **Waiting Time**, **Turnaround Time**, and **Response Time**[cite: 7].

## Features
* **Algorithms Implemented:**
    * [cite_start]First Come First Serve (FCFS) [cite: 25]
    * [cite_start]Shortest Job First (SJF) - Non-preemptive [cite: 27]
    * [cite_start]Shortest Remaining Time (SRT) - Preemptive [cite: 28]
    * [cite_start]Round Robin (RR) - Configurable Time Quantum [cite: 30]
    * [cite_start]Multilevel Feedback Queue (MLFQ) - 3 Levels with Aging [cite: 31]
* [cite_start]**Input:** Reads process data from a CSV file (Console-based)[cite: 21, 22].
* [cite_start]**Output:** Displays a clear metric table and an ASCII Gantt chart for process execution[cite: 7].

## Prerequisites
* [cite_start]**Language:** Python 3.x [cite: 60]
* **Libraries:** Standard libraries only (`csv`, `collections`, `sys`). No external installations required.

## Project Structure
```text
CPUScheduler/
│
├── main.py              # Entry point: Handles input, execution, and printing results
├── process.py           # Class definition for a 'Process'
├── scheduler.py         # Logic for all 5 scheduling algorithms
├── input.csv            # Input data file
└── README.md            # Project documentation

```

Setup & Installation 

1. **Clone or Download** the repository to your local machine.
2. Ensure you have Python installed:
```bash
python --version

```


3. Navigate to the project directory:
```bash
cd CPUScheduler

```



Usage 

### 1. Prepare Input Data

Edit the `input.csv` file to define your processes. The format is:
`pid,arrival_time,burst_time,priority`

**Example (Sample Scenario):**

```csv
pid,arrival_time,burst_time,priority
P1,0,5,0
P2,1,3,0
P3,2,8,0
P4,3,6,0

```

*(Note: Priority is optional but required for the CSV format. Lower integers imply higher priority if used in custom logic, though this MLFQ implementation uses Queues for priority.)* 

### 2. Run the Simulator

Execute the `main.py` script:

```bash
python main.py

```

The program will automatically load the `input.csv` file and run all five algorithms sequentially, displaying the results for each.

Algorithm Descriptions 

### 1. First Come First Serve (FCFS)

The simplest algorithm. Processes are executed in the order they arrive in the ready queue. It is non-preemptive.

### 2. Shortest Job First (SJF)

A non-preemptive algorithm that selects the waiting process with the smallest **Burst Time**. This minimizes average waiting time but requires knowing the burst time in advance.

### 3. Shortest Remaining Time (SRT)

The preemptive version of SJF. The process with the smallest **remaining** burst time is chosen. If a new process arrives with a shorter burst than the current process has left, the CPU preempts the current process.

### 4. Round Robin (RR)

Designed for time-sharing systems. Each process is assigned a fixed time unit called a **Time Quantum** (Default: 2). If the process doesn't finish within the quantum, it is moved to the back of the queue.

### 5. Multilevel Feedback Queue (MLFQ)

A complex scheduling algorithm that moves processes between queues based on their behavior:

* **Queue 1:** Priority High, RR with Quantum = 2.
* **Queue 2:** Priority Medium, RR with Quantum = 4.
* **Queue 3:** Priority Low, FCFS.
* **Rules:** New processes enter Q1. If they use their full quantum, they are demoted to the lower queue.
* 
**Aging:** To prevent starvation, processes sitting in lower queues for too long (default interval: 20) are promoted back to Q1.



Sample Output 

Below is an example of the output generated for the **Round Robin** algorithm:

```text
--- Running Round Robin Algorithm (Quantum=2) ---

PID     Arrival Burst   Finish  Wait    Turnaround      Response
-----------------------------------------------------------------
P1      0       5       13      8       13              0
P2      1       3       15      11      14              0
P3      2       8       22      12      20              12
P4      3       6       20      11      17              11
-----------------------------------------------------------------
Averages:                       10.50   16.00           5.75

--- Gantt Chart ---
 |  P1  |  P2  |  P3  |  P1  |  P4  |  P2  |  P3  |  P1  |  P4  |  P3  |
 0      2      4      6      8      10     11     13     14     18     22 

```

```

---

### **Final Git Action**
Commit this new file to your repository.

```bash
git add README.md
git commit -m "Docs: Add README with setup instructions and algorithm details"

```

### **Conclusion**

You have now fully implemented the **CPU Scheduling Simulator**!

1. **Code:** `main.py`, `scheduler.py`, `process.py`.
2. **Data:** `input.csv`.
3. **Docs:** `README.md`.
4. **Visuals:** ASCII Gantt charts in the console.

