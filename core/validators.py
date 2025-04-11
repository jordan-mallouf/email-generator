from datetime import datetime

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
            return f"{float_val:.2f}"  # Always returns a formatted string
        except ValueError:
            print("Please enter a valid number for the amount.")

# Input validation for input dates
def get_valid_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, '%m/%d/%Y')
            return value
        except ValueError:
            print("Invalid date format. Please use MM/DD/YYYY (e.g., 04/10/2025).")