# Importstdlib
from datetime import date
import os
import pathlib

# Import external libraries
from pylatex import (
    Document,
    Head,
    Foot,
    LargeText,
    LineBreak,
    MiniPage,
    PageStyle,
    Package,
    Section,
    StandAloneGraphic,
    Tabular,
    VerticalSpace
    )
from pylatex.base_classes import Environment
from pylatex.utils import (
    NoEscape, 
    bold
    )

GEOMETRY_OPTIONS = {
    "head": "40pt",
    "margin": "0.5in",
    "bottom": "1.6in",
    "includeheadfoot": True
    }

class Form(Environment):
    """A class to wrap hyperref's form environment."""

    _latex_name = 'Form'

    packages = [Package('hyperref')]
    escape = False
    content_separator = "\n"


class PdfGen:
    def __init__(self) -> None:
        # Document Geometry Options and Creation
        self.geometry_options = GEOMETRY_OPTIONS
        self.doc = Document(geometry_options=self.geometry_options)

    def generate_files(self, data, **kwargs):
        ...

    def add_header(self, page: PageStyle) -> None:
        """
        Generate document and add a header to it
        """
        # self.first_page = PageStyle("firstpage")

        # Right Header: Image
        with page.create(Head("L")) as header_left:
            with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                             pos='c')) as logo_wrapper:
                logo_file = os.path.join(os.path.dirname(__file__),
                                         'andolina-logo.png')
                logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
                                                      filename=logo_file))

        # Left Header: Document Title
        with page.create(Head("R")) as right_header:
            with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                pos='c',
                                                align='l')) as title_wrapper:
                self.document_title(title_wrapper)
        
        self.doc.append(VerticalSpace('20ex'))

    def document_title(self, title_wrapper):
        ...
    
    def add_footer(self, page: PageStyle):
        """
        Generate footer. For the time being, with LOPD & School adress
        """
        with page.create(Foot("L")) as footer:
            self.footer(footer)
    
    def footer(self, footer: Foot):
        ...
    
    def generate_additional_details(self):
        """
        Add details. For now, payment formula & IVA exemption.
        """
        with self.doc.create(Section('', numbering=False)):
            self.additional_details()

    def additional_details(self):
        ...
    
    def generate_file(self,
                      filename: str = 'test'):
        """Generate pdf file

        Args:
            filename (str, optional): _description_. Defaults to 'test'.
            mode (str, optional): Defines if it must generate
                an invoice or a detailed extract.
                Defaults to 'invoice'.
        """
        path_to_bills = pathlib.Path(__file__).parent.resolve().joinpath(f'bills/{filename}')
        self.doc.generate_pdf(path_to_bills,
                              clean_tex=True)


class Billing:
    def generate_associate_table(self, name, NIF, adress):
        """
        Add associate information to file as table
        """
        with self.doc.create(Tabular('l|l',
                                        row_height=1.2)) as associate_table:
            associate_table.add_row([bold("Nombre:"), name])
            associate_table.add_hline()
            associate_table.add_row([bold("NIF:"), NIF])
            associate_table.add_hline()
            associate_table.add_row([bold("Dirección:"), adress])
            associate_table.add_hline()

        self.doc.append(VerticalSpace('8ex'))