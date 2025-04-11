import os
from core.validators import get_required_input

def ensure_output_dir(path='output'):
    # Create the output directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

def generate_filename(name, invoice_number):
    # Return a clean filename based on name and invoice number
    return f"{name.replace(' ', '_')}_{invoice_number}.txt"

def check_filename(output_dir, filename):
    full_path = os.path.join(output_dir, filename)
    if os.path.exists(full_path):
        print(f"'{filename}' already exists.")
        new_name = get_required_input("Enter a new filename: ")
        filename = f"{new_name}.txt"
        full_path = os.path.join(output_dir, filename)
    return full_path, filename

def save_email(email_text, output_path):
    # Save email to output/
    with open(output_path, 'w') as f:
        f.write(email_text)