import os
from datetime import datetime
from core.generator import (load_template, generate_email, list_templates, select_template)
from core.validators import(get_required_input, get_currency_input, get_valid_date)

def main():
    # Initialize the current date
    today = datetime.today().strftime('%m/%d/%Y')
    templates = list_templates()
    template_path = select_template(templates)
    template = load_template(template_path)

    # Gather input from user
    name = get_required_input("Enter the recipient's name: ")
    date = today
    amount = get_currency_input("Enter the amount of the invoice: $")
    invoice_number = get_required_input("Enter an invoice number: ")
    details = input("Enter any additional details (press Enter to skip): ")

    # Extra input if using 'Invoice or Reminder' template
    if 'invoice' in template_path.lower() or 'reminder' in template_path.lower():
        due_date = get_valid_date("Enter the due date of the invoice: ")

    # Extra input if using 'Thank-You' template
    if 'thanks' in template_path.lower():
        payment_date = get_valid_date("Enter the payment date: ")
        new_amount = get_currency_input("Enter the payment amount: $")

    # Data dictionary
    values = {
        "name": name,
        "date": date,
        "amount": amount,
        "invoice_number": invoice_number,
        "details": details or ""
    }

    if 'invoice' in template_path.lower() or 'reminder' in template_path.lower():
        values["due_date"] = due_date
        
    if 'thanks' in template_path.lower():
        values["payment_date"] = payment_date
        values["new_amount"] = new_amount

    email = generate_email(template, values)
    
    # Generates confirmation message
    print("\nEmail Preview:")
    print("=" * 40)
    print(email)
    print("=" * 40)

    # Preview the proposed filename before confirmation
    proposed_filename = f"{values['name'].replace(' ','_')}_{values['invoice_number']}.txt"
    print(f"Proposed filename: {proposed_filename}")

    # Confirmation before saving email as a .txt file
    confirm = input("Would you like to save this email as a .txt file? (y/n): ").strip().lower()

    if confirm == 'y':
        os.makedirs('output', exist_ok=True)
        output_path = os.path.join('output', proposed_filename)

        # Check if file exists
        if os.path.exists(output_path):
            new_filename = get_required_input("File name already exists. Please enter a new filename: ")
            proposed_filename = f"{new_filename}.txt"
            output_path = os.path.join('output', proposed_filename)

        with open(output_path, 'w') as f:
            f.write(email)

        print(f"Email saved to output folder as: {proposed_filename}")
    else:
        print("Email was not saved.")

if __name__ == "__main__":
    main()
