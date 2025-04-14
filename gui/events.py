import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from core import generate_email, generate_filename, check_filename, ensure_output_dir, save_email
import os
from gui.layout import input_fields

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