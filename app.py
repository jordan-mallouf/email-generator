def load_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()
    
def generate_email(template_str, data):
    return template_str.format(**data)

def main():
    template_path = 'template/default.txt'
    template = load_template(template_path)

    # Example data
    values = {
        "name":"Jordan Mallouf",
        "date": "4/10/2025",
        "amount": 150.00,
        "invoice_number": 123456,
        "details": "This invoice covers your monthly fraternity dues for April."
    }

    email = generate_email(template, values)
    print(email)

if __name__ == "__main__":
    main()