import psutil
import time
import customtkinter as ctk
from threading import Thread
from math import pi, cos, sin
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------ SETĂRI UI ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("System Monitor")
app.geometry("1000x700")

FONT_BIG = ("Consolas", 18)
FONT_MED = ("Consolas", 16)

# ------------------ VARIABILE TRAFIC ------------------
last_net = psutil.net_io_counters()
cpu_data = []

# ------------------ FUNCȚII ------------------
def format_bytes(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:6.2f} {unit}"
        bytes /= 1024

def get_top_processes():
    processes = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top_cpu = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:5]
    top_ram = sorted(processes, key=lambda p: p['memory_info'].rss, reverse=True)[:5]
    return top_cpu, top_ram

# ------------------ CEAS ANALOG ------------------
def draw_analog(canvas, x, y, size, value, label):
    """Desenează un ceas analog cu gradaje 0-100 și cifre vizibile mai aproape de cerc"""
    canvas.delete(label)
    radius = size // 2

    # Cerc exterior
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, width=2, outline="blue", tags=label)

    # Gradaje și numere
    for i in range(0, 100, 10):
        angle = (i / 100) * 2 * pi - pi/2
        # Liniile gradajului
        x0 = x + cos(angle) * radius * 0.85
        y0 = y + sin(angle) * radius * 0.85
        x1 = x + cos(angle) * radius * 0.95
        y1 = y + sin(angle) * radius * 0.95
        canvas.create_line(x0, y0, x1, y1, fill="white", width=2, tags=label)

        # Numerele mai aproape, offset redus
        offset = 12  # distanța suplimentară față de cerc
        x_text = x + cos(angle) * (radius + offset)
        y_text = y + sin(angle) * (radius + offset)
        canvas.create_text(x_text, y_text, text=str(i), fill="cyan", font=("Consolas", 10), tags=label)

    # Indicator
    angle = (value / 100) * 2 * pi - pi/2
    x_end = x + cos(angle) * radius * 0.9
    y_end = y + sin(angle) * radius * 0.9
    canvas.create_line(x, y, x_end, y_end, fill="red", width=3, tags=label)

    # Label central
    canvas.create_text(x, y + radius + 30, text=label, fill="white", font=FONT_MED, tags=label)





def update_analog(cpu, ram, disk, net_down):
    draw_analog(clock_canvas, 100, 100, 80, cpu, "CPU")
    draw_analog(clock_canvas, 300, 100, 80, ram.percent, "RAM")
    draw_analog(clock_canvas, 500, 100, 80, disk.percent, "SSD")
    draw_analog(clock_canvas, 700, 100, 80, min(net_down / 1024 / 1024 * 10, 100), "NET")

# ------------------ UPDATE UI ------------------
def update_ui(cpu, ram, disk, down, up, cpu_text, ram_text):
    cpu_label.configure(text=f"CPU:      {cpu:5.1f} %")
    ram_label.configure(text=f"RAM:      {format_bytes(ram.used)} / {format_bytes(ram.total)}")
    disk_label.configure(text=f"SSD:      {format_bytes(disk.used)} / {format_bytes(disk.total)}")
    net_label.configure(text=f"NET:      ↓ {format_bytes(down)}/s   ↑ {format_bytes(up)}/s")
    cpu_proc_label.configure(text=cpu_text)
    ram_proc_label.configure(text=ram_text)

    cpu_data.append(cpu)
    if len(cpu_data) > 30:
        cpu_data.pop(0)

    ax.clear()
    ax.plot(cpu_data)
    ax.set_ylim(0, 100)
    ax.set_title("CPU Usage (%)")
    canvas.draw()

    update_analog(cpu, ram, disk, down)

def update_stats():
    global last_net
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        down = net.bytes_recv - last_net.bytes_recv
        up = net.bytes_sent - last_net.bytes_sent
        last_net = net

        top_cpu, top_ram = get_top_processes()
        cpu_text = "Top CPU Apps:\n" + "\n".join(f"{p['name'][:20]:20} {p['cpu_percent']:6.1f}%" for p in top_cpu)
        ram_text = "Top RAM Apps:\n" + "\n".join(f"{p['name'][:20]:20} {format_bytes(p['memory_info'].rss)}" for p in top_ram)

        app.after(0, update_ui, cpu, ram, disk, down, up, cpu_text, ram_text)
        time.sleep(1)

# ------------------ UI ------------------
frame = ctk.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=20, pady=20)

# Canvas pentru ceasuri
clock_canvas = ctk.CTkCanvas(frame, width=800, height=200, bg="#222222", highlightthickness=0)
clock_canvas.pack(pady=10)

cpu_label = ctk.CTkLabel(frame, font=FONT_BIG, width=450, anchor="w")
cpu_label.pack(pady=5)

ram_label = ctk.CTkLabel(frame, font=FONT_BIG, width=450, anchor="w")
ram_label.pack(pady=5)

disk_label = ctk.CTkLabel(frame, font=FONT_BIG, width=450, anchor="w")
disk_label.pack(pady=5)

net_label = ctk.CTkLabel(frame, font=FONT_BIG, width=450, anchor="w")
net_label.pack(pady=5)

cpu_proc_label = ctk.CTkLabel(frame, font=FONT_MED, justify="left", width=500, anchor="w")
cpu_proc_label.pack(pady=10)

ram_proc_label = ctk.CTkLabel(frame, font=FONT_MED, justify="left", width=500, anchor="w")
ram_proc_label.pack(pady=10)

# ------------------ GRAFIC CPU ------------------
fig = Figure(figsize=(7, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_ylim(0, 100)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(pady=20)

# ------------------ THREAD ------------------
Thread(target=update_stats, daemon=True).start()

app.mainloop()
