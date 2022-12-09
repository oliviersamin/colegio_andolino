import os

from pylatex import Command, Document, NoEscape, Package
from pylatex.base_classes import Environment

class Form(Environment):
    """A class to wrap hyperref's form environment."""

    _latex_name = 'Form'

    packages = [Package('hyperref')]
    escape = False
    content_separator = "\n"

doc = Document()

with doc.create(Form()):
    doc.append(Command('noindent'))
    doc.append(Command('TextField',
               options=[NoEscape("width=\linewidth"),"height=1in"],
               arguments=['Name:','male'],))
doc.append('Hey')
file = 'demo'
doc.generate_pdf(os.path.join(os.path.dirname(__file__),
                              file),
                 clean_tex=False)
# doc.generate_tex('demo')