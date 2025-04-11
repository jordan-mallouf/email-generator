import os

def load_template(template_path):
    # Load contents of template file as a string
    with open(template_path, 'r') as file:
        return file.read()
    
def generate_email(template_str, data):
    # Substitute placeholders in template with actual data
    return template_str.format(**data)

def list_templates(template_dir='templates'):
    # Lists available templates in the directory
    return [f for f in os.listdir(template_dir) if f.endswith('.txt')]

def select_template(template_list):
    # Displays templates and returns the selected one
    print("Available Templates:")
    for i, filename in enumerate(template_list, start=1):
        print(f"{i}. {filename}")

    while True:
        choice = input("Select a template by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(template_list):
            return os.path.join('templates', template_list[int(choice) - 1])
        else:
            print("Invalid choice, Please choose a valid template!")