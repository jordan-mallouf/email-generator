import os

def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()
    
def generate_email(template_str, data):
    return template_str.format(**data)

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

def main():
    template_path = select_template()
    template = load_template(template_path)

    # Gather input from user
    name = input("Enter the recipient's name: ")
    date = input("Enter the date of the email: ")
    amount = input("Enter the amount of the invoice: $")
    invoice_number = input("Enter an invoice number: ")
    details = input("Enter any additional details (press Enter to skip): ")

    # Extra input if using 'Thank-You' template
    if 'thanks' in template_path.lower():
        payment_date = input("Enter the payment date: ")
        new_amount = input("Enter the payment amount: $")

    # Example data
    values = {
        "name": name,
        "date": date,
        "amount": amount,
        "invoice_number": invoice_number,
        "details": details or "" # since details is optional
    }

    if 'thanks' in template_path.lower():
        values["payment_date"] = payment_date
        values["new_amount"] = new_amount

    email = generate_email(template, values)
    print(email)

if __name__ == "__main__":
    main()