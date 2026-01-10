import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from process import Process
from scheduler import solve_fcfs, solve_sjf, solve_srt, solve_rr, solve_mlfq
import csv

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x800")
        
        # Store processes
        self.process_list = []
        
        # --- UI LAYOUT ---
        
        # 1. Control Panel (Top)
        control_frame = tk.LabelFrame(root, text="Configuration", padx=10, pady=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Algorithm Selection
        tk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
        self.algo_var = tk.StringVar()
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var, state="readonly")
        self.algo_combo['values'] = ("FCFS", "SJF (Non-Preemptive)", "SRT (Preemptive)", "Round Robin", "MLFQ")
        self.algo_combo.current(0)
        self.algo_combo.grid(row=0, column=1, padx=5)
        
        # Quantum Input (Only for RR)
        tk.Label(control_frame, text="Quantum:").grid(row=0, column=2, padx=5)
        self.quantum_entry = tk.Entry(control_frame, width=5)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=0, column=3, padx=5)
        
        # Aging Interval for MLFQ
        tk.Label(control_frame, text="Aging Interval (MLFQ):").grid(row=0, column=4, padx=5)
        self.aging_entry = tk.Entry(control_frame, width=5)
        self.aging_entry.insert(0, "20")
        self.aging_entry.grid(row=0, column=5, padx=5)
        
        # Run Button
        tk.Button(control_frame, text="Run Simulation", command=self.run_simulation, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=6, padx=10)
        
        # Export Button
        tk.Button(control_frame, text="Export Results", command=self.export_results,
                 bg="#2196F3", fg="white").grid(row=0, column=7, padx=10)
        
        # Reset Button
        tk.Button(control_frame, text="Reset", command=self.reset_data, 
                 bg="#f44336", fg="white").grid(row=0, column=8, padx=10)

        # 2. Tabbed Interface for Input Methods
        input_notebook = ttk.Notebook(root)
        input_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: CSV Import
        csv_tab = ttk.Frame(input_notebook)
        input_notebook.add(csv_tab, text="CSV Import")
        
        # CSV Import Controls
        csv_control_frame = tk.Frame(csv_tab)
        csv_control_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(csv_control_frame, text="Browse CSV File", command=self.load_csv).pack(side="left", padx=5)
        tk.Button(csv_control_frame, text="Load Example CSV", command=self.load_example).pack(side="left", padx=5)
        
        # CSV Display
        csv_display_frame = tk.LabelFrame(csv_tab, text="Loaded CSV Data")
        csv_display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("PID", "Arrival", "Burst", "Priority")
        self.csv_tree = ttk.Treeview(csv_display_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.csv_tree.heading(col, text=col)
            self.csv_tree.column(col, width=80, anchor="center")
        
        csv_scroll = ttk.Scrollbar(csv_display_frame, orient="vertical", command=self.csv_tree.yview)
        self.csv_tree.configure(yscrollcommand=csv_scroll.set)
        
        self.csv_tree.pack(side="left", fill="both", expand=True)
        csv_scroll.pack(side="right", fill="y")
        
        # Tab 2: Manual Input
        manual_tab = ttk.Frame(input_notebook)
        input_notebook.add(manual_tab, text="Manual Input")
        
        # Manual Input Controls
        manual_control_frame = tk.Frame(manual_tab)
        manual_control_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(manual_control_frame, text="PID:").grid(row=0, column=0, padx=5)
        self.pid_entry = tk.Entry(manual_control_frame, width=10)
        self.pid_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(manual_control_frame, text="Arrival Time:").grid(row=0, column=2, padx=5)
        self.arrival_entry = tk.Entry(manual_control_frame, width=10)
        self.arrival_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(manual_control_frame, text="Burst Time:").grid(row=0, column=4, padx=5)
        self.burst_entry = tk.Entry(manual_control_frame, width=10)
        self.burst_entry.grid(row=0, column=5, padx=5)
        
        tk.Label(manual_control_frame, text="Priority:").grid(row=0, column=6, padx=5)
        self.priority_entry = tk.Entry(manual_control_frame, width=10)
        self.priority_entry.insert(0, "0")
        self.priority_entry.grid(row=0, column=7, padx=5)
        
        tk.Button(manual_control_frame, text="Add Process", command=self.add_manual_process,
                 bg="#4CAF50", fg="white").grid(row=0, column=8, padx=10)
        
        tk.Button(manual_control_frame, text="Clear All", command=self.clear_manual_input,
                 bg="#ff9800", fg="white").grid(row=0, column=9, padx=5)
        
        # Manual Input Display
        manual_display_frame = tk.LabelFrame(manual_tab, text="Manual Processes")
        manual_display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.manual_tree = ttk.Treeview(manual_display_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.manual_tree.heading(col, text=col)
            self.manual_tree.column(col, width=80, anchor="center")
        
        manual_scroll = ttk.Scrollbar(manual_display_frame, orient="vertical", command=self.manual_tree.yview)
        self.manual_tree.configure(yscrollcommand=manual_scroll.set)
        
        self.manual_tree.pack(side="left", fill="both", expand=True)
        manual_scroll.pack(side="right", fill="y")
        
        # Quick Load Example Button
        example_frame = tk.Frame(manual_tab)
        example_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(example_frame, text="Load Example Processes", 
                 command=self.load_manual_example).pack(side="left")
        
        # 3. Results Section
        results_frame = tk.LabelFrame(root, text="Simulation Results")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Results Tree
        res_columns = ("PID", "Start", "Finish", "Wait", "Turnaround", "Response")
        self.result_tree = ttk.Treeview(results_frame, columns=res_columns, show="headings", height=8)
        for col in res_columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=80, anchor="center")
        
        result_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=result_scroll.set)
        
        self.result_tree.pack(side="left", fill="both", expand=True)
        result_scroll.pack(side="right", fill="y")
        
        # 4. Gantt Chart Area (Bottom)
        gantt_frame = tk.LabelFrame(root, text="Gantt Chart Visualization")
        gantt_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(gantt_frame, bg="white", height=120)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar for Gantt
        self.gantt_scroll = tk.Scrollbar(gantt_frame, orient="horizontal", command=self.canvas.xview)
        self.gantt_scroll.pack(fill="x")
        self.canvas.configure(xscrollcommand=self.gantt_scroll.set)

    def load_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filename:
            return
            
        self.process_list = []
        # Clear existing
        for item in self.csv_tree.get_children():
            self.csv_tree.delete(item)
            
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    p = Process(row['pid'], int(row['arrival_time']), 
                               int(row['burst_time']), int(row['priority']))
                    self.process_list.append(p)
                    self.csv_tree.insert("", "end", values=(p.pid, p.arrival_time, 
                                                          p.burst_time, p.priority))
            messagebox.showinfo("Success", f"Loaded {len(self.process_list)} processes from CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def load_example(self):
        # Create example CSV content
        example_data = [
            ["P1", 0, 5, 0],
            ["P2", 1, 3, 0],
            ["P3", 2, 8, 0],
            ["P4", 3, 6, 0]
        ]
        
        self.process_list = []
        for item in self.csv_tree.get_children():
            self.csv_tree.delete(item)
            
        for data in example_data:
            p = Process(data[0], data[1], data[2], data[3])
            self.process_list.append(p)
            self.csv_tree.insert("", "end", values=(p.pid, p.arrival_time, 
                                                  p.burst_time, p.priority))
        messagebox.showinfo("Example Loaded", "Loaded example CSV data with 4 processes")

    def add_manual_process(self):
        try:
            pid = self.pid_entry.get().strip()
            arrival = int(self.arrival_entry.get().strip())
            burst = int(self.burst_entry.get().strip())
            priority = int(self.priority_entry.get().strip())
            
            if not pid:
                messagebox.showwarning("Warning", "PID cannot be empty!")
                return
                
            # Check for duplicate PID
            for p in self.process_list:
                if p.pid == pid:
                    messagebox.showwarning("Warning", f"PID '{pid}' already exists!")
                    return
            
            p = Process(pid, arrival, burst, priority)
            self.process_list.append(p)
            
            # Add to manual tree
            self.manual_tree.insert("", "end", values=(pid, arrival, burst, priority))
            
            # Clear input fields
            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.priority_entry.insert(0, "0")
            
            # Auto-focus next input
            self.pid_entry.focus_set()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for arrival, burst, and priority!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add process: {e}")

    def clear_manual_input(self):
        # Clear only the manual tree, not the entire process list
        for item in self.manual_tree.get_children():
            self.manual_tree.delete(item)
        
        # Remove manual processes from process_list
        # We'll keep a separate list or use tags next time, but for simplicity:
        # Rebuild process_list from CSV tree only
        temp_list = []
        for item in self.csv_tree.get_children():
            values = self.csv_tree.item(item)['values']
            p = Process(values[0], values[1], values[2], values[3])
            temp_list.append(p)
        self.process_list = temp_list
        
        messagebox.showinfo("Cleared", "Manual input cleared!")

    def load_manual_example(self):
        example_processes = [
            ["P1", 0, 5, 0],
            ["P2", 1, 3, 0],
            ["P3", 2, 8, 0],
            ["P4", 3, 6, 0]
        ]
        
        # Clear existing manual input first
        for item in self.manual_tree.get_children():
            self.manual_tree.delete(item)
        
        for proc in example_processes:
            self.manual_tree.insert("", "end", values=tuple(proc))
            p = Process(proc[0], proc[1], proc[2], proc[3])
            self.process_list.append(p)
        
        messagebox.showinfo("Example Loaded", "Loaded 4 example processes to manual input")

    def reset_data(self):
        self.process_list = []
        for tree in [self.csv_tree, self.manual_tree, self.result_tree]:
            for item in tree.get_children():
                tree.delete(item)
        self.canvas.delete("all")
        messagebox.showinfo("Reset", "All data has been reset!")

    def run_simulation(self):
        if not self.process_list:
            messagebox.showwarning("Warning", "No processes loaded! Add processes via CSV or Manual Input.")
            return
            
        # Get Algorithm
        algo = self.algo_var.get()
        
        # CREATE DEEP COPY of list to avoid modifying original input data
        sim_processes = []
        for p in self.process_list:
            sim_processes.append(Process(p.pid, p.arrival_time, p.burst_time, p.priority))
            
        result_procs = []
        gantt_data = []
        
        try:
            if algo == "FCFS":
                result_procs, gantt_data = solve_fcfs(sim_processes)
            elif algo == "SJF (Non-Preemptive)":
                result_procs, gantt_data = solve_sjf(sim_processes)
            elif algo == "SRT (Preemptive)":
                result_procs, gantt_data = solve_srt(sim_processes)
            elif algo == "Round Robin":
                q = int(self.quantum_entry.get())
                result_procs, gantt_data = solve_rr(sim_processes, q)
            elif algo == "MLFQ":
                aging = int(self.aging_entry.get())
                result_procs, gantt_data = solve_mlfq(sim_processes, aging_interval=aging)
                
            self.display_results(result_procs)
            self.draw_gantt_chart(gantt_data)
            
            # Show summary
            avg_wait = sum(p.waiting_time for p in result_procs) / len(result_procs)
            avg_turn = sum(p.turnaround_time for p in result_procs) / len(result_procs)
            messagebox.showinfo("Simulation Complete", 
                              f"Algorithm: {algo}\n"
                              f"Processes: {len(result_procs)}\n"
                              f"Avg Wait Time: {avg_wait:.2f}\n"
                              f"Avg Turnaround Time: {avg_turn:.2f}")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check your input values: {e}")
        except Exception as e:
            messagebox.showerror("Simulation Error", str(e))

    def display_results(self, processes):
        # Clear previous results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
            
        # Calculate averages
        total_wait = sum(p.waiting_time for p in processes)
        total_turn = sum(p.turnaround_time for p in processes)
        total_response = sum(p.response_time for p in processes)
        count = len(processes)
        
        avg_wait = total_wait / count if count > 0 else 0
        avg_turn = total_turn / count if count > 0 else 0
        avg_response = total_response / count if count > 0 else 0
        
        # Insert process results
        for p in processes:
            self.result_tree.insert("", "end", values=(
                p.pid, p.start_time, p.completion_time, 
                p.waiting_time, p.turnaround_time, p.response_time
            ))
            
        # Insert Average row with different background
        self.result_tree.insert("", "end", values=(
            "AVG", "", "", 
            f"{avg_wait:.2f}", f"{avg_turn:.2f}", f"{avg_response:.2f}"
        ), tags=('avg',))
        
        self.result_tree.tag_configure('avg', background='#e6f3ff', font=('Arial', 10, 'bold'))

    def draw_gantt_chart(self, gantt_data):
        self.canvas.delete("all")
        
        if not gantt_data:
            self.canvas.create_text(300, 60, text="No Gantt chart data available", 
                                   font=("Arial", 12), fill="gray")
            return
        
        start_x = 20
        y = 30
        height = 40
        scale = 40  # pixels per time unit
        
        # Color palette for PIDs
        colors = ["#ff9999", "#99ccff", "#99ff99", "#ffff99", "#ffcc99", 
                 "#cc99ff", "#ff99cc", "#99ffcc", "#ccff99", "#ffccff"]
        pid_color_map = {}
        
        max_time = 0
        
        # Draw process blocks
        for pid, start, end in gantt_data:
            duration = end - start
            width = duration * scale
            
            x0 = start_x + (start * scale)
            x1 = x0 + width
            
            # Assign color
            if pid not in pid_color_map:
                color_idx = len(pid_color_map) % len(colors)
                pid_color_map[pid] = colors[color_idx]
            
            # Draw Rectangle
            self.canvas.create_rectangle(x0, y, x1, y+height, 
                                       fill=pid_color_map[pid], 
                                       outline="black", 
                                       width=2)
            
            # Draw Text (PID)
            self.canvas.create_text((x0+x1)/2, y+height/2, 
                                  text=pid, 
                                  font=("Arial", 10, "bold"))
            
            # Draw Time Markers at start
            self.canvas.create_text(x0, y+height+15, 
                                  text=str(start), 
                                  font=("Arial", 8))
            
            max_time = max(max_time, end)
        
        # Final time marker
        self.canvas.create_text(start_x + (max_time * scale), y+height+15, 
                              text=str(max_time), 
                              font=("Arial", 8))
        
        # Draw timeline
        self.canvas.create_line(start_x, y+height+25, 
                              start_x + (max_time * scale), y+height+25, 
                              width=2)
        
        # Legend
        legend_x = start_x
        legend_y = y + height + 40
        for i, (pid, color) in enumerate(pid_color_map.items()):
            x_pos = legend_x + (i * 80)
            self.canvas.create_rectangle(x_pos, legend_y, x_pos+20, legend_y+15, 
                                       fill=color, outline="black")
            self.canvas.create_text(x_pos+30, legend_y+7, 
                                  text=pid, 
                                  font=("Arial", 9), 
                                  anchor="w")
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def export_results(self):
        if not self.process_list:
            messagebox.showwarning("Warning", "No results to export!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Re-run simulation to get fresh results
                algo = self.algo_var.get()
                sim_processes = []
                for p in self.process_list:
                    sim_processes.append(Process(p.pid, p.arrival_time, p.burst_time, p.priority))
                
                if algo == "FCFS":
                    result_procs, _ = solve_fcfs(sim_processes)
                elif algo == "SJF (Non-Preemptive)":
                    result_procs, _ = solve_sjf(sim_processes)
                elif algo == "SRT (Preemptive)":
                    result_procs, _ = solve_srt(sim_processes)
                elif algo == "Round Robin":
                    q = int(self.quantum_entry.get())
                    result_procs, _ = solve_rr(sim_processes, q)
                elif algo == "MLFQ":
                    aging = int(self.aging_entry.get())
                    result_procs, _ = solve_mlfq(sim_processes, aging_interval=aging)
                
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write header
                    writer.writerow(["CPU Scheduling Simulation Results"])
                    writer.writerow(["Algorithm:", algo])
                    writer.writerow([])
                    writer.writerow(["PID", "Arrival", "Burst", "Priority", 
                                   "Start", "Finish", "Wait", "Turnaround", "Response"])
                    
                    # Write data
                    for p in result_procs:
                        writer.writerow([
                            p.pid, p.arrival_time, p.burst_time, p.priority,
                            p.start_time, p.completion_time,
                            p.waiting_time, p.turnaround_time, p.response_time
                        ])
                    
                    # Write averages
                    writer.writerow([])
                    avg_wait = sum(p.waiting_time for p in result_procs) / len(result_procs)
                    avg_turn = sum(p.turnaround_time for p in result_procs) / len(result_procs)
                    avg_response = sum(p.response_time for p in result_procs) / len(result_procs)
                    
                    writer.writerow(["Averages", "", "", "", "", "", 
                                   f"{avg_wait:.2f}", f"{avg_turn:.2f}", f"{avg_response:.2f}"])
                
                messagebox.showinfo("Success", f"Results exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()