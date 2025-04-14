# Email Generator (CLI & GUI)

A simple Python application for generating templated emails through a graphical user interface.
Ideal for quickly writing and saving emails such as invoices, reminders and thank-you confirmations.
This tool was built with modularity, simplicity, and usability in mind.

## Features
- Select from customizable '.txt' templates
- Dynamically rendered input fields based on template selection
- Auto-filled date field (uses today's date)
- Input Validation:
  -  Required Fields
  -  Numeric Fields (e.g. amount, invoice number)
  -  Date Fields (must follow 'MM/DD/YYYY')
- Email preview before saving
- File-saving options:
  -  Overwrite existing files
  - Rename and re-save if conflicts occur

# Project Structure
Email-Generator/
* core
  * generator.py - Handles all logic regarding loading, listing, and selecting templates; Also generates the email preview.
  * io.py - Ensures that the '.txt' file is saved in outputs/ when completed successfully.
  * validators.py - Validates the inputs for the CLI application.
* gui
  * events.py - Allows for the generation, preview and saving of the email in the GUI.
  * layout.py - Displays templates and fields for the GUI.
  * widgets.py - An extra file for extra features that might be added.
* templates
  * invoice.txt - Basic invoice template.
  * reminder.txt - Basic reminder template.
  * thanks.txt - Basic thank-you template.
* app.py - CLI Application
* main.py - GUI Application

## How to Use
1. Make sure you have at least Python 3.10 installed
2. Clone this repository:
   ```bash
   git clone https://github.com/jordan-mallouf/email-generator.git
   cd email-generator
   ```
3. Launch the application
   ```bash
   ./app.py OR ./main.py
   OR
   python3 -m app.py OR python3 -m main.py
   ```
4. Inside the app:
*   Select a template
*   Fill out the form
*   Preview and save the email
5. View outputs/ folder for saved email (If not already created, one will be created during runtime)!

## Example Template: Invoice
```
SUBJECT: Invoice #{invoice_number}

Hi {name},

This is a reminder that your invoice of ${amount} is due on {due_date}.

{details}

Best,
The Production Team
production@team.com
(123) 456-7890
```
You can even add your own templates in the templates/ directory using the {placeholder} syntax!

## Requirements
* Python 3.10 or newer
* Standard library only (uses built-in tkinter)

## Author
Developed by Jordan Mallouf
