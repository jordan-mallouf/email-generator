def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()
    
def generate_email(template_str, data):
    return template_str.format(**data)

def main():
    template_path = 'templates/default.txt'
    template = load_template(template_path)

    # Gather input from user
    name = input("Enter the recipient's name: ")
    date = input("Enter the date of the email: ")
    amount = input("Enter the amount of the invoice: ")
    invoice_number = input("Enter an invoice number: ")
    details = input("Enter any additional details (press Enter to skip): ")

    # Example data
    values = {
        "name": name,
        "date": date,
        "amount": amount,
        "invoice_number": invoice_number,
        "details": details or "" # since details is optional
    }

    email = generate_email(template, values)
    print(email)

if __name__ == "__main__":
    main()