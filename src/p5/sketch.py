import os
import sys
from IPython.core.display import HTML
from IPython.core.magic import register_cell_magic
from jinja2 import Environment, FileSystemLoader, select_autoescape

_template_path = os.path.join(sys.prefix, 'p5_data')

env = Environment(
    loader=FileSystemLoader(_template_path),
    autoescape=select_autoescape()
)

def transpile(code):
    template = env.get_template("sketch.html")
    fmt_code = 'from p5 import *\n' + code + '\nrun()'
    html = template.render(code=fmt_code)
    return html

def write_html(name, html):
    sketch_folder = os.path.join(os.getcwd(), 'sketches')
    if not os.path.isdir(sketch_folder):
        os.makedirs(sketch_folder)
    filename = os.path.join(sketch_folder, f'{name}.html')
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        print(html, file=f)
    return filename

def run(name, code):
    html = transpile(code)
    filename = write_html(name, html)
    sketch = HTML(filename=filename)
    display(sketch)

@register_cell_magic
def sketch(line, cell):
    code = cell
    name = line
    run(name, code)
