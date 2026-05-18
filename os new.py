import tkinter as tk
from tkinter import messagebox
import random


class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.color = self.generate_color()
        self.waiting_time = 0
        self.turnaround_time = 0

    def generate_color(self):
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]
        return random.choice(colors)



def run_fcfs_logic(processes):
    processes.sort(key=lambda x: x.arrival)
    current_time = 0
    chart_data = []
    for p in processes:
        if current_time < p.arrival: current_time = p.arrival
        start = current_time
        end = start + p.burst
        p.waiting_time = start - p.arrival
        p.turnaround_time = end - p.arrival
        chart_data.append((p.pid, start, end, p.color))
        current_time = end
    return chart_data



def run_sjf_logic(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    chart_data = []
    ready_queue = []
    visited = [False] * n

    while completed < n:

        for i in range(n):
            if processes[i].arrival <= current_time and not visited[i]:
                ready_queue.append(processes[i])
                visited[i] = True

        if ready_queue:

            ready_queue.sort(key=lambda x: x.burst)
            p = ready_queue.pop(0)

            start = current_time
            end = start + p.burst
            p.waiting_time = start - p.arrival
            p.turnaround_time = end - p.arrival
            chart_data.append((p.pid, start, end, p.color))
            current_time = end
            completed += 1
        else:
            current_time += 1
    return chart_data



def run_round_robin_logic(processes, quantum):
    processes.sort(key=lambda x: x.arrival)
    current_time = 0
    chart_data = []
    rem_burst = {p.pid: p.burst for p in processes}
    colors = {p.pid: p.color for p in processes}
    finish_times = {}
    ready_queue = []
    completed = 0
    n = len(processes)
    visited = set()

    while completed < n:
        for p in processes:
            if p.arrival <= current_time and p.pid not in visited:
                ready_queue.append(p)
                visited.add(p.pid)

        if not ready_queue:
            current_time += 1
            continue
        curr_p = ready_queue.pop(0)
        exec_time = min(rem_burst[curr_p.pid], quantum)
        chart_data.append((curr_p.pid, current_time, current_time + exec_time, colors[curr_p.pid]))

        current_time += exec_time
        rem_burst[curr_p.pid] -= exec_time
        for p in processes:
            if p.arrival <= current_time and p.pid not in visited:
                ready_queue.append(p)
                visited.add(p.pid)
        if rem_burst[curr_p.pid] > 0:
            ready_queue.append(curr_p)
        else:
            finish_times[curr_p.pid] = current_time
            completed += 1
    for p in processes:
        p.turnaround_time = finish_times[p.pid] - p.arrival
        p.waiting_time = p.turnaround_time - p.burst
    return chart_data



class FinalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator - 3 Algorithms")
        self.root.geometry("900x800")
        self.processes = []


        frame = tk.LabelFrame(root, text=" إدخال العمليات ", pady=10)
        frame.pack(pady=10, fill="x", padx=20)
        tk.Label(frame, text="PID:").grid(row=0, column=0)
        self.e_pid = tk.Entry(frame, width=10);
        self.e_pid.grid(row=0, column=1)
        tk.Label(frame, text="Arrival:").grid(row=0, column=2)
        self.e_arr = tk.Entry(frame, width=10);
        self.e_arr.grid(row=0, column=3)
        tk.Label(frame, text="Burst:").grid(row=0, column=4)
        self.e_brst = tk.Entry(frame, width=10);
        self.e_brst.grid(row=0, column=5)
        tk.Button(frame, text="إضافة", command=self.add, bg="blue", fg="white").grid(row=0, column=6, padx=10)
        tk.Button(frame, text="مسح", command=self.reset, bg="red", fg="white").grid(row=0, column=7)


        opt = tk.Frame(root)
        opt.pack(pady=10)
        self.algo = tk.StringVar(value="FCFS")
        tk.OptionMenu(opt, self.algo, "FCFS", "Round Robin", "SJF").pack(side=tk.LEFT)
        tk.Label(opt, text=" Quantum: ").pack(side=tk.LEFT)
        self.e_q = tk.Entry(opt, width=5);
        self.e_q.insert(0, "2");
        self.e_q.pack(side=tk.LEFT)
        tk.Button(root, text="تشغيل المحاكاة", command=self.draw, bg="green", fg="white", font=("Arial", 12)).pack(
            pady=10)

        self.canvas = tk.Canvas(root, width=850, height=150, bg="white", border=2, relief="ridge")
        self.canvas.pack(pady=10)
        self.res = tk.Text(root, height=12, width=90);
        self.res.pack(pady=10)

    def add(self):
        try:
            self.processes.append(Process(self.e_pid.get(), int(self.e_arr.get()), int(self.e_brst.get())))
            self.e_pid.delete(0, tk.END);
            self.e_arr.delete(0, tk.END);
            self.e_brst.delete(0, tk.END)
        except:
            messagebox.showerror("خطأ", "بيانات خاطئة")

    def reset(self):
        self.processes = [];
        self.canvas.delete("all");
        self.res.delete("1.0", tk.END)
    def draw(self):
        if not self.processes: return
        self.canvas.delete("all");
        self.res.delete("1.0", tk.END)
        choice = self.algo.get()
        if choice == "FCFS":
            data = run_fcfs_logic(self.processes[:])
        elif choice == "SJF":
            data = run_sjf_logic(self.processes[:])
        else:
            data = run_round_robin_logic(self.processes[:], int(self.e_q.get()))

        x, y, s = 40, 40, 25
        for pid, st, en, c in data:
            self.canvas.create_rectangle(x + st * s, y, x + en * s, y + 50, fill=c)
            self.canvas.create_text(x + (st + en) * s / 2, y + 25, text=pid, fill="white")
            self.canvas.create_text(x + st * s, y + 70, text=str(st))
            if data.index((pid, st, en, c)) == len(data) - 1: self.canvas.create_text(x + en * s, y + 70, text=str(en))

        self.res.insert(tk.END,
                        f"{'Process':<10} | {'Arrival':<10} | {'Burst':<10} | {'Wait':<10} | {'TAT':<10}\n" + "-" * 65 + "\n")
        tw, tt = 0, 0
        for p in self.processes:
            self.res.insert(tk.END,
                            f"{p.pid:<10} | {p.arrival:<10} | {p.burst:<10} | {p.waiting_time:<10} | {p.turnaround_time:<10}\n")
            tw += p.waiting_time;
            tt += p.turnaround_time
        self.res.insert(tk.END,
                        f"\nAverage Waiting Time: {tw / len(self.processes):.2f}\nAverage Turnaround Time: {tt / len(self.processes):.2f}")


if __name__ == "__main__":
    root = tk.Tk();
    FinalApp(root);
    root.mainloop()