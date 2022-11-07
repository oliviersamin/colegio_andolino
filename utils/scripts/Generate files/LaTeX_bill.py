'''
This file produces a pdf
https://stackoverflow.com/a/8086042
'''

# Import stdlib
import argparse
import os
import subprocess
import sys


# Read base TeX file as string
__location__ = os.path.realpath(os.path.join(os.path.dirname(__file__), 'base.tex'))
with open(__location__, 'r') as file:
    content = file.read()#.replace('\n', '')

# Produce dict to populate LaTeX file
# Use argparse to accept values or
# generate dict
if len(sys.argv) > 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--course')
    parser.add_argument('-t', '--title')
    parser.add_argument('-n', '--name',) 
    parser.add_argument('-s', '--school', default='My U')

    args = parser.parse_args()
else:
    ...

# Fill LaTeX file
with open('bill.tex','w') as f:
    f.write(content%args.__dict__)

# Use subprocess to call pdflatex cover.tex
cmd = ['pdflatex', '-interaction', 'nonstopmode', 'bill.tex']
proc = subprocess.Popen(cmd)
proc.communicate()

# Check for errors generating pdf file
retcode = proc.returncode
if not retcode == 0:
    os.unlink('bill.pdf')
    raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 

# Remove unneeded files
os.unlink('bill.tex')
os.unlink('bill.log')



# LaTeX table
def generate_table(rows,col_align='lr'):
    '''
    generate a table string to write to the tex file
    '''
    backslash = '\\'
    row_string = (len(col_align)-1) * '& ' + 2*backslash
    rows_string = rows * row_string
    string = f'{backslash}begin{{table}}[]\n' + \
             f'{backslash}begin{{tabular}}{col_align}\n' + \
             f'{rows_string[:-2]}\n' + \
             f'{backslash}end{{tabular}}\n' + \
             f'{backslash}end{{table}}\n'

    return string
