import tkinter as tk
from gui import *

# Main GUI Launcher
def launch_gui():
    window = tk.Tk()
    window.title("Email Generator")
    window.geometry("700x700")

    tk.Label(window, text="Email Generator", font=("Helvetica", 16)).pack(pady=10)

    template_frame = tk.Frame(window)
    template_frame.pack()

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    preview_box = tk.Text(window, width=80, height=15)
    preview_box.pack(pady=10)

    def on_template_selected(template_name):
        nonlocal current_template
        current_template = open(f"templates/{template_name}").read()
        render_fields(template_name, input_frame)

    current_template = ""
    select_template_gui(template_frame, on_template_selected)

    tk.Button(window, text="Generate Email", command=lambda: generate_and_preview_email(current_template, preview_box)).pack(pady=5)
    tk.Button(window, text="Save Email", command=lambda: save_email_gui(preview_box)).pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    launch_gui()