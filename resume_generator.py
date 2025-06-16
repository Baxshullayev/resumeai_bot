
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import tempfile

def generate_resume_pdf(user_data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resume_template.html')
    html_out = template.render(user_data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        HTML(string=html_out).write_pdf(pdf_file.name)
        return pdf_file.name
