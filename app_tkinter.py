import tkinter as tk
from tkinter import ttk
import threading, time, webbrowser, requests

API_URL = "http://127.0.0.1:5000/api/stats_local"

def open_web():
    webbrowser.open("http://127.0.0.1:5000")

def updater():
    while True:
        try:
            r = requests.get(API_URL, timeout=3)
            if r.status_code == 200:
                data = r.json()
                cpu_label.config(text=f"CPU: {data['cpu']}%")
                ram_label.config(text=f"RAM: {data['ram_percent']}%")
                disk_label.config(text=f"Disque: {data['disk_percent']}%")
            else:
                cpu_label.config(text="CPU: --")
                ram_label.config(text="RAM: --")
                disk_label.config(text="Disque: --")
        except Exception:
            cpu_label.config(text="CPU: --")
            ram_label.config(text="RAM: --")
            disk_label.config(text="Disque: --")
        time.sleep(3)

root = tk.Tk()
root.title("SysWatch - Mini Monitor")
root.geometry("320x180")
root.resizable(False, False)

ttk.Label(root, text="SysWatch (local)", font=("Arial", 14, "bold")).pack(pady=8)
cpu_label = ttk.Label(root, text="CPU: --", font=("Arial", 12))
ram_label = ttk.Label(root, text="RAM: --", font=("Arial", 12))
disk_label = ttk.Label(root, text="Disque: --", font=("Arial", 12))
cpu_label.pack(); ram_label.pack(); disk_label.pack()
ttk.Button(root, text="Ouvrir Dashboard Web", command=open_web).pack(pady=10)

threading.Thread(target=updater, daemon=True).start()
root.mainloop()
