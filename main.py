import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from core import list_templates, generate_email, generate_filename, check_filename, ensure_output_dir, save_email
from datetime import datetime
import os

input_fields = {}

# Select a template
def select_template_gui(container, on_select_callback):
    tk.Label(container, text="Select a Template").pack()

    templates = list_templates()
    selected_template = tk.StringVar()
    dropdown = ttk.Combobox(container, textvariable=selected_template, values=templates, state="readonly")
    dropdown.pack()

    def handle_selection(event):
        template_name = selected_template.get()
        on_select_callback(template_name)

    dropdown.bind("<<ComboboxSelected>>", handle_selection)
    return selected_template

# Render the fields based on template chosen
def render_fields(template_name, container):
    global input_fields
    input_fields.clear()

    for widget in container.winfo_children():
        widget.destroy()

    if "invoice" in template_name.lower() or "reminder" in template_name.lower():
        fields = ["name", "amount", "invoice_number", "due_date", "details"]
    elif "thanks" in template_name.lower():
        fields = ["name", "invoice_number", "payment_date", "new_amount", "details"]
    else:
        fields = []

    for field in fields:
        label = tk.Label(container, text=field.replace("_", " ").title())
        label.pack()
        entry = tk.Entry(container, width=50)
        entry.pack()
        input_fields[field] = entry

# Generate email preview
def generate_and_preview_email(template_str, preview_box):
    data = {}
    for field, entry in input_fields.items():
        val = entry.get().strip()
        
        # Validating inputs
        if field == "name":
            if not val:
                preview_box.delete("1.0", tk.END)
                preview_box.insert(tk.END, "Name is required.")
                return
            data[field] = val
        
        elif field == "amount":
            if not val:
                preview_box.delete("1.0", tk.END)
                preview_box.insert(tk.END, "Amount is required.")
                return
            try:
                data[field] = f"{float(val):.2f}"
            except ValueError:
                preview_box.delete("1.0", tk.END)
                preview_box.insert(tk.END, "Amount must be a valid number.")
                return
            
        elif field == "invoice_number":
            if not val:
                preview_box.delete("1.0", tk.END)
                preview_box.insert(tk.END, "Invoice Number is required.")
                return
            try:
                int(val) # Validates integer
                data[field] = val
            except ValueError:
                preview_box.delete("1.0", tk.END)
                preview_box.insert(tk.END, "Invoice Number must be an integer.")
                return      
        
        elif field in ["due_date", "payment_date"]:
            if val:
                try:
                    datetime.strptime(val, "%m/%d/%Y")
                    data[field] = val
                except ValueError:
                    preview_box.delete("1.0", tk.END)
                    preview_box.insert(tk.END, f"{field.replace('_', ' ').title()} must be in MM/DD/YYYY format.")
                    return
        
        elif field == "new_amount":
            if val:
                try:
                    data[field] = f"{float(val):.2f}"
                except ValueError:
                    preview_box.delete("1.0", tk.END)
                    preview_box.insert(tk.END, "New Amount must be a valid number.")
                    return            
        
        else:
            data[field] = val or ""

    data["date"] = datetime.today().strftime('%m/%d/%Y')
    
    try:
        result = generate_email(template_str, data)
        preview_box.delete("1.0", tk.END)
        preview_box.insert(tk.END, result)
    except KeyError as e:
        preview_box.delete("1.0", tk.END)
        preview_box.insert(tk.END, f"[ERROR] Missing placeholder in template: {e}")

# Save email
def save_email_gui(preview_box):
    email_text = preview_box.get("1.0", tk.END).strip()
    if not email_text:
        print("Nothing to save.")
        return

    name = input_fields.get("name").get().strip()
    invoice = input_fields.get("invoice_number").get().strip()

    if not name or not invoice:
        print("Missing name or invoice number - can't create filename.")
        return

    filename = generate_filename(name, invoice)
    ensure_output_dir()
    
    # Logic for file saving
    output_dir = 'output'
    output_path, final_filename = check_filename(output_dir, filename)

    # If file exists, ask user if they want to overwrite, rename or cancel the saved file
    while os.path.exists(output_path):
        choice = messagebox.askyesnocancel("File Exists!", f"'{final_filename}' already exists. \n\nWould you like to overwrite it?")
        if choice is True:
            # Overwrite
            break
        elif choice is False:
            # Rename
            new_filename = simpledialog.askstring("New Filename", "Enter a new filename:")
            if not new_filename:
                print("Save cancelled.")
                return
            final_filename = f"{new_filename}.txt"
            output_path = os.path.join(output_dir, final_filename)
        else:
            # Cancelled
            print("Save Cancelled.")
            return    

    # Confirm Save
    confirm = messagebox.askyesno("Confirm Save", f"Save as '{final_filename}'?")
    if not confirm:
        print("Cancelled.")
        return

    save_email(email_text, output_path)
    messagebox.showinfo("Success", f"Saved to: {output_path}")

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