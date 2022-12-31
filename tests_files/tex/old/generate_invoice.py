'''
This file produces a pdf
https://stackoverflow.com/a/8086042


# Read base TeX file as string
__location__ = os.path.realpath(os.path.join(os.path.dirname(__file__), 'base.tex'))
with open(__location__, 'r') as file:
content = file.read()#.replace('\n', '')
'''

# Import stdlib
import argparse
import os
import subprocess
import shutil
import sys

# Import external libraries
from numpy import nan


# Define global variables
PRECIO_UNITARIO_COMEDOR = 5
PRECIO_MAX_COMEDOR = 20
PRECIO_UNITARIO_ATENCION_TEMPRANA = 5
PRECIO_MAX_ATENCION_TEMPRANA = 20


def parse_args():
    '''
    Produce dict to populate LaTeX file
    Use argparse to accept values or generate dict
    '''
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--course')
        parser.add_argument('-t', '--title')
        parser.add_argument('-n', '--name',)
        parser.add_argument('-s', '--school', default='My U')

        arguments = parser.parse_args()
    else:
        arguments = {}

    return arguments

def fill_tex_file(name, date, args):
    '''
    Copy invoice_template.tex, rename file and fill with args
    '''
    # Copy file
    source = 'invoice_template.tex'
    target = f'invoice_{name}_{date}'

    shutil.copy(source, target)

    __location__ = os.path.realpath(os.path.join(os.path.dirname(__file__), target))
    with open(__location__,'w',encoding=str) as f:
        content = f.read()
        f.write(content%args.__dict__)

def generate_pdf():
    '''
    Use subprocess to call pdflatex cover.tex
    '''
    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'bill.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    # Check for errors generating pdf file
    retcode = proc.returncode
    if retcode != 0:
        os.unlink('bill.pdf')
        raise ValueError(f'Error {retcode} executing command: {cmd}') 

    # Remove unneeded files
    os.unlink('bill.tex')
    os.unlink('bill.log')


# LaTeX table
def generate_extract(use: dict) -> dict:
    '''
    concepts = ["Atención temprana", "Acompañamiento", "Extracurricular 1", "Extracurricular 2", "Extracurricular 3", "Extracurricular 4",
                "Comedor", "Cuota", "Formaciones", "Talleres, actividades y campamentos", "Otros"]
    quantity = [3,5,1,nan,nan,nan,
                10,2,"15€","20€","10€"]
    data = dict(zip(concepts,quantity))
    '''
    basic_concepts = ["Atención temprana", "Acompañamiento", "Extracurricular 1", "Extracurricular 2", "Extracurricular 3", "Extracurricular 4",
                      "Comedor", "Cuota", "Formaciones", "Talleres, actividades y campamentos"]
    for key in use.keys():
        if key == "Comedor":
            bill_dinning(use[key])
            
            
def bill_dinning(num):
    '''
    Compute the expense of dinning room
    '''
    
    
def generate_table(rows,col_align='lr'):
    '''
    generate a table string to write to the tex file
    backslash = '\\'
    row_string = (len(col_align)-1) * '& ' + 2*backslash
    rows_string = rows * row_string
    string = f'{backslash}begin{{table}}[]\n' + \
             f'{backslash}begin{{tabular}}{col_align}\n' + \
             f'{rows_string[:-2]}\n' + \
             f'{backslash}end{{tabular}}\n' + \
             f'{backslash}end{{table}}\n'
    '''
    table = '''\\begin{table}[h]
    \\centering
    \\begin{tabular}{l | a | b | a }
    \\hline
    \\rowcolor{LightCyan}
    \\mc{1}{concepto} & \\mc{1}{coste unitario} & \\mc{1}{cantidad} & \\mc{1}{coste}\\ 
    \\hline
    variable 1 & a & b & c \\\\ \\hline
    variable 2 & a & b & c \\\\ \\hline
    \\end{tabular}
    \\end{table}'''

    return string

if __name__ == '__main__':
    args = parse_args()

    fill_tex_file(name,date,args)
    generate_pdf()
    