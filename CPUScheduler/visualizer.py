import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

def plot_gantt_chart(gantt_data):
    """
    Plots a Gantt chart using Matplotlib.
    gantt_data: List of tuples (PID, Start, End)
    """
    if not gantt_data:
        print("No data to plot.")
        return

    # 1. Setup Data for Plotting
    # We need to group start/durations by PID to plot them on the same 'y' line
    # Format for broken_barh: (start_time, duration)
    process_intervals = {}
    all_pids = set()
    
    for pid, start, end in gantt_data:
        duration = end - start
        if duration == 0: continue
        
        if pid not in process_intervals:
            process_intervals[pid] = []
        process_intervals[pid].append((start, duration))
        all_pids.add(pid)
        
    # Sort PIDs to make the Y-axis orderly (e.g., P1 at top or bottom)
    sorted_pids = sorted(list(all_pids), key=lambda x: int(x[1:]) if x[1:].isdigit() else x)
    
    # 2. Setup Figure
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Generate distinct colors
    colors = list(mcolors.TABLEAU_COLORS.values())
    pid_color_map = {pid: colors[i % len(colors)] for i, pid in enumerate(sorted_pids)}

    # 3. Plot Bars
    # Y-position: We give each PID a height level (10, 20, 30...)
    y_start = 10
    y_height = 9
    yticks = []
    yticklabels = []
    
    for i, pid in enumerate(sorted_pids):
        # Y position for this process
        y_pos = y_start + (i * 10)
        
        # Data for this process
        intervals = process_intervals[pid]
        
        # Plot
        ax.broken_barh(intervals, (y_pos, y_height), facecolors=pid_color_map[pid], edgecolors='black')
        
        # Label placement
        yticks.append(y_pos + y_height/2)
        yticklabels.append(pid)
        
        # Add labels inside the bars for clarity
        for start, duration in intervals:
            center_x = start + duration/2
            center_y = y_pos + y_height/2
            ax.text(center_x, center_y, pid, ha='center', va='center', color='white', fontweight='bold', fontsize=8)

    # 4. Formatting
    ax.set_ylim(5, 5 + len(sorted_pids) * 10 + 5)
    ax.set_xlim(0, max(end for _, _, end in gantt_data) + 2)
    ax.set_xlabel('Time Units')
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    ax.set_title('CPU Scheduling Gantt Chart')
    
    plt.tight_layout()
    plt.show()