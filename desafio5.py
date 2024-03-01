import tkinter as tk
from tkinter import messagebox
import socket

def scan_ports(host, start_port, end_port, ports):
    open_ports = []
    if ports:  
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    s.connect((host, port))
                    open_ports.append(port)
            except (socket.timeout, ConnectionRefusedError):
                pass
    else: 
        for port in range(start_port, end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    s.connect((host, port))
                    open_ports.append(port)
            except (socket.timeout, ConnectionRefusedError):
                pass
    return open_ports

def scan():
    host = host_entry.get()
    start_port_str = start_port_entry.get()
    end_port_str = end_port_entry.get()
    ports_str = ports_entry.get()

    if not host:
        messagebox.showerror("Error", "Please enter a host or IP address.")
        return

    try:
        start_port = int(start_port_str) if start_port_str else None
        end_port = int(end_port_str) if end_port_str else None
        if start_port and end_port and start_port >= end_port:
            messagebox.showerror("Error", "End port must be greater than start port.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid port format.")
        return

    if ports_str:
        try:
            ports = [int(port.strip()) for port in ports_str.split(",")]
            for port in ports:
                if port < 1 or port > 65535:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid port format or value.")
            return
    else:
        ports = []

    open_ports = scan_ports(host, start_port, end_port, ports)
    result_text.delete(1.0, tk.END)
    for port in open_ports:
        service = services.get(port, "Unknown")
        result_text.insert(tk.END, f"Port {port}: {service}\n")

services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP Proxy",
}

background_color = "#c45d18"
button_bg = "black"
button_fg = "white"

root = tk.Tk()
root.title("Port Scanner")
root.configure(bg=background_color)

host_label = tk.Label(root, text="Host or IP:", bg=background_color, fg="black")
host_label.grid(row=0, column=0, sticky="s")
start_port_label = tk.Label(root, text="Start Port:", bg=background_color, fg="black")
start_port_label.grid(row=1, column=0, sticky="s")
end_port_label = tk.Label(root, text="End Port:", bg=background_color, fg="black")
end_port_label.grid(row=2, column=0, sticky="s")
ports_label = tk.Label(root, text="Ports (comma-separated):", bg=background_color, fg="black")
ports_label.grid(row=3, column=0, sticky="s")

host_entry = tk.Entry(root, bg=button_fg, fg="black", highlightcolor=background_color)
host_entry.grid(row=0, column=1)
start_port_entry = tk.Entry(root, bg=button_fg, fg="black", highlightcolor=background_color)
start_port_entry.grid(row=1, column=1)
end_port_entry = tk.Entry(root, bg=button_fg, fg="black", highlightcolor=background_color)
end_port_entry.grid(row=2, column=1)
ports_entry = tk.Entry(root, bg=button_fg, fg="black", highlightcolor=background_color)
ports_entry.grid(row=3, column=1)

scan_button = tk.Button(root, text="Scan Ports", command=scan, bg=button_bg, fg=button_fg)
scan_button.grid(row=4, columnspan=2)

result_text = tk.Text(root, height=7, width=40, bg=button_fg, fg="black")
result_text.grid(row=5, columnspan=2, sticky="nsew")

root.mainloop()
