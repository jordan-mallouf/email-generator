# core/__init__.py
from .generator import (load_template, generate_email, list_templates, select_template)
from .validators import(get_required_input, get_currency_input, get_valid_date)
from .io import(ensure_output_dir, generate_filename, check_filename, save_email)
