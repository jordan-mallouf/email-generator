import tkinter as tk
from tkinter import ttk
from core import list_templates

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