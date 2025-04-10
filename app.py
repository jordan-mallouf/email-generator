import os
from datetime import datetime

# Loads template
def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()
    
def generate_email(template_str, data):
    return template_str.format(**data)

# Logic for selecting template
def select_template():
    templates = [f for f in os.listdir('templates') if f.endswith('.txt')]
    print("Available Templates:")
    for i, filename in enumerate(templates, start=1):
        print(f"{i}. {filename}")

    while True:
        choice = input("Select a template by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(templates):
            return os.path.join('templates', templates[int(choice) - 1])
        else:
            print("Invalid choice. Please enter a valid option!")

# Input validation for required inputs
def get_required_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please try again!")

# Input validation for currency
def get_currency_input(prompt):
    while True:
        value = input(prompt).replace("$", "").strip()
        try:
            float_val = float(value)
            return f"{float_val:.2f}" # Always returns a formatted string
        except ValueError:
            print("Please enter a valid number for the amount.")

def main():
    # Initialize the current date
    today = datetime.today().strftime('%m/%d/%Y')
    template_path = select_template()
    template = load_template(template_path)

    # Gather input from user
    name = get_required_input("Enter the recipient's name: ")
    date = today
    amount = get_currency_input("Enter the amount of the invoice: $")
    invoice_number = get_required_input("Enter an invoice number: ")
    details = input("Enter any additional details (press Enter to skip): ")

    # Extra input if using 'Invoice or Reminder' template
    if 'invoice' in template_path.lower() or 'reminder' in template_path.lower():
        due_date = get_required_input("Enter the due date of the invoice: ")

    # Extra input if using 'Thank-You' template
    if 'thanks' in template_path.lower():
        payment_date = get_required_input("Enter the payment date: ")
        new_amount = get_currency_input("Enter the payment amount: $")

    # Data dictionary
    values = {
        "name": name,
        "date": date,
        "amount": amount,
        "invoice_number": invoice_number,
        "details": details or "" # since details is optional
    }

    if 'invoice' in template_path.lower() or 'reminder' in template_path.lower():
        values["due_date"] = due_date
        
    if 'thanks' in template_path.lower():
        values["payment_date"] = payment_date
        values["new_amount"] = new_amount

    email = generate_email(template, values)
    print(email)

if __name__ == "__main__":
    main()