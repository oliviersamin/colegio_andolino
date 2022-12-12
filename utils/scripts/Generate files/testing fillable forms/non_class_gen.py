'''
Generate pdf files with pylatex
for invoices or detailed extracts.
'''
# import stdlib
import calendar
from datetime import date
from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import chain
from json import dumps as jdumps
from json import loads as jloads
import locale
from typing import Literal
import os

# import external libs
import numpy as np
from pylatex import (Command, Document, Foot, FootnoteText, Head, HugeText, LargeText, LineBreak,
                     LongTabu, MiniPage, NoEscape, Package, PageStyle, Section, StandAloneGraphic, Subsection,
                     Tabular, VerticalSpace, TextColor)
from pylatex.utils import NoEscape, bold, dumps_list
from pylatex.base_classes import Environment

# Constants
from constants import (
    ACTIVIDADES,
    COLEGIO_DATOS,
    COLEGIO_NOMBRE,
    UNIT_PRICE,
    UNIT_PRICES_DICT,
    CASES,
    CLAUSULA_PROT_DATOS,
    CLAUSULA_PROT_DATOS_PERSONAL,
    CONS_CLAUS_PROT_DATOS_PERSONAL,
    LOPD_COOP,
    CONFIDENCIALIDAD,
    POL_PROT_DATOS,
    PUB_IMAG,
    LOPD,
    VERSION_LOPD,
    INFO_DATOS_MEDICOS,
    ACTIVITIES_COLORS_DICT
)


CONS_CLAUS_PROT_DATOS_PERSONAL = os.getenv('CONS_CLAUS_PROT_DATOS_PERSONAL',
                                           "D/Dª …………………………………………………………………………………………………………, "
                                           "con NIF o pasaporte Nº ………………………… como titular o representante legal del mismo, "
                                           "consiente de forma inequívoca la presente cláusula "
                                           "y política de privacidad de protección de datos de carácter personal:"
                                           )



class Form(Environment):
    """A class to wrap hyperref's form environment."""

    _latex_name = 'Form'

    packages = [Package('hyperref')]
    escape = False
    content_separator = "\n"



class PdfGen():
    def __init__(self, mode:str, data:list) -> None:
        self.mode = mode
        self.data = data
        # Document Geometry Options
        self.geometry_options = {
            "head": "40pt",
            "margin": "0.5in",
            "bottom": "1.6in",
            "includeheadfoot": True
        }
        
        
        # dates
        self.invoice_date = date.today()
        self.year = self.invoice_date.year
        self.month = self.invoice_date.month
        current_year_formated = self.year % 100
        self.current_academic_year = (f"{current_year_formated}"
                                      f"{current_year_formated + 1}")

    def generate_files(self, data, **kwargs):
        match self.mode:
            case 'invoice':
                # basic file data
                self.series = kwargs.series
                self.invoice_num_start = kwargs.invoice_num_start
                self.current_invoice_num = kwargs.invoice_num_start
                assert all(isinstance(associate,Associate) for associate in data), f'{TypeError} {data} is not of Associate type'
                for associate_data in self.associates_data:
                    self.fill_file(associate_data)
            case 'extract':
                assert all(isinstance(student,Student) for student in data), f'{TypeError} {data} is not of Students type'
                for students in data:
                    self.fill_file(associate_data=students.associate,
                                   kids_data=students.children)
            case _:
                self.fill_file()
            # case 'enrollment':
            # case 'direct debit':
            # case 'LOPD':
            # case 'image posting':
            # case 'school outings':
            # case 'health report':

    def fill_file(self):
        self.header()
        self.footer()
        self.doc.preamble.append(self.first_page)
        self.body()
        self.generate_file()

    def generate_file(self,
                      filename: str = 'test',
                      mode: str = 'invoice'):
        """Generate pdf file

        Args:
            filename (str, optional): _description_. Defaults to 'test'.
            mode (str, optional): Defines if it must generate
                an invoice or a detailed extract.
                Defaults to 'invoice'.
        """
        # Format page
        self.doc.change_document_style("firstpage")
        self.doc.add_color(name="lightgray", model="gray", description="0.80")

        # Generate pdf
        file = f"./{self.current_associate_data['invoice_num']}" if mode == 'invoice' else \
               f"./{self.current_associate_data['invoice_num']}_extract" if mode == 'extract' else \
               filename
        self.doc.generate_pdf(os.path.join(os.path.dirname(__file__),
                                           file),
                              clean_tex=True)

    def header(self,) -> None:
        """
        Generate document and add a header to it
        """
        self.doc = Document(geometry_options=self.geometry_options)

        self.first_page = PageStyle("firstpage")

        # Header image
        with self.first_page.create(Head("L")) as header_left:
            with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                             pos='c')) as logo_wrapper:
                logo_file = os.path.join(os.path.dirname(__file__),
                                         'andolina-logo.png')
                logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
                                                      filename=logo_file))

        match self.mode:
            case 'invoice':
                # Add document title
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        self.generate_invoice_id()
                        title_wrapper.append(LargeText(bold(f"Número de factura: {self.current_associate_data['invoice_num']}")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LargeText(bold(f"Fecha: {self.current_associate_data['date']}")))
            case 'extract':
                # Add document title
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        self.generate_invoice_id()
                        title_wrapper.append(LargeText(bold(f"Extracto de factura: {self.current_associate_data['invoice_num']}")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LargeText(bold(f"Fecha: {self.current_associate_data['date']}")))
            case 'enrollment':
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        title_wrapper.append(HugeText(bold("Impreso de Matrícula")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        with title_wrapper.create(Form()):
                            title_wrapper.append(Command('noindent'))
                            title_wrapper.append(Command('TextField',
                                               options=[NoEscape("width=\linewidth"),
                                                        "height=1in"],
                                               arguments='Curso: '))
            case 'direct debit':
                pass
            case 'LOPD':
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        title_wrapper.append(LargeText(bold("Cláusula LOPD")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(TextColor('black',
                                                    LargeText(bold("SOCIOS COOPERATIVISTAS"))))
            case 'image posting':
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        title_wrapper.append(LargeText(bold("Autorización para")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(TextColor('black',
                                                    LargeText(bold("publicación de imágenes"))))
            case 'school outings':
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        title_wrapper.append(LargeText(bold("Autorización Salidas Escolares")))
            case 'health report':
                with self.first_page.create(Head("R")) as right_header:
                    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                                      pos='c',
                                                      align='l')) as title_wrapper:
                        title_wrapper.append(LargeText(bold("Información de Salud - Alergias")))
                        title_wrapper.append(LineBreak())
                        title_wrapper.append(LineBreak())
                        with title_wrapper.create(Form()):
                            title_wrapper.append(Command('noindent'))
                            title_wrapper.append(Command('TextField',
                                               options=[NoEscape("width=\linewidth"),
                                                        "height=1in"],
                                               arguments='Curso: '))

        self.doc.append(VerticalSpace('8ex'))

    def generate_invoice_id(self) -> str:
        '''
        Get current invoice number formated
        Example: FU-2223-001
        '''
        self.current_associate_data['invoice_num'] = f'{self.series}-{self.current_academic_year}-{self.current_invoice_num:03}'
        self.current_invoice_num += 1
        self.current_associate_data['date'] = self.invoice_date.strftime("%d/%m/%y")

    def footer(self,):
        """
        Generate footer. For the time being, with LOPD & School adress
        """
        match self.mode:
            case 'invoice' | 'extract':
                with self.first_page.create(Foot("L")) as footer:
                    footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))
            # case 'extract':
            #     with self.first_page.create(Foot("L")) as footer:
            #         footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))
            case 'enrollment':
                with self.first_page.create(Foot("L")) as footer:
                    footer.append(FootnoteText(f"{COLEGIO_NOMBRE}"))
            case 'direct debit':
                pass
            case 'LOPD':
                with self.first_page.create(Foot("L")) as footer:
                    footer.append(FootnoteText(f"{COLEGIO_NOMBRE}\n\n{VERSION_LOPD}"))
            case 'image posting':
                pass
            case 'school outings':
                with self.first_page.create(Foot("L")) as footer:
                    footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))
            case 'health report':
                with self.first_page.create(Foot("L")) as footer:
                    footer.append(FootnoteText(f"{INFO_DATOS_MEDICOS}\n\n\n{COLEGIO_DATOS}"))

    def body(self):
        match self.mode:
            case 'invoice':
                self.generate_associate_table()
                # self.doc.preamble.append(self.first_page)
                self.generate_invoice_table()
                self.generate_additional_details()
            case 'extract':
                self.generate_associate_table()
                # self.doc.preamble.append(self.first_page)
                self.generate_detailed_calendar()
            case 'enrollment':
                self.student_section()
                self.parents_section()
                self.LOPD_section()
            case 'direct debit':
                pass
            case 'LOPD':
                self.LOPD_coop_section()
            case 'image posting':
                self.image_posting_table()
                self.image_posting_LOPD()
            case 'school outings':
                self.parent_autorization()
            case 'health report':
                self.health_info()

    def generate_associate_table(self):
        """
        Add associate information to file as table
        """
        with self.doc.create(Tabular('l|l',
                                     row_height=1.2)) as associate_table:
            associate_table.add_row([bold("Nombre:"), self.current_associate_data['name']])
            associate_table.add_hline()
            associate_table.add_row([bold("NIF:"), self.current_associate_data['NIF']])
            associate_table.add_hline()
            associate_table.add_row([bold("Dirección:"), self.current_associate_data['adress']])
            associate_table.add_hline()

        self.doc.append(VerticalSpace('8ex'))

    def generate_invoice_table(self):
        """
        Generate a table with the extract for current invoice
        """
        with self.doc.create(LongTabu("X[3l] X[c] X[c] X[c]",
                                      row_height=1.5)) as invoice_table:
            invoice_table.add_row(["concepto",
                                   "precio unitario",
                                   "cantidad",
                                   "subtotal"],
                                  mapper=bold,
                                  color="lightgray")
            invoice_table.add_empty_row()

            extract_final = self.generate_extract()
            for row in extract_final:
                invoice_table.add_hline()
                invoice_table.add_row(row)

            self.doc.append(VerticalSpace('10ex'))

    def generate_extract(self) -> list[tuple]:
        """
        Generate current extract data into a list of rows (tuples).

        Returns:
            list[tuple]: _description_
        """
        '''
        concepts = ["Atención temprana", "Acompañamiento",
                    "Extracurricular 1", "Extracurricular 2",
                    "Extracurricular 3", "Extracurricular 4",
                    "Comedor", "Cuota", "Formaciones",
                    "Talleres, actividades y campamentos", "Otros"]
        quantity = [3, 5, 1, 0, 0, 0, 10, 2, "15€", "20€"]
        data = dict(zip(concepts,quantity))
        '''
        basic_concepts = ["CUOTA",
                          "COMEDOR",
                          "ATENCIÓN_TEMPRANA",
                          "JUDO",
                          "CIENCIA",
                          "TEATRO",
                          "ROBOTIX",
                          "ACOMPAÑAMIENTO",
                          "FORMACIONES",
                          "TALLERES_ACTIVIDADES_CAMPAMENTOS"]
        test_quantity = [3, (5, 2), (1, 0), 0, 0, 0, 10, "6€", "15€", "20€"]
        use = dict(zip(basic_concepts,
                       test_quantity))

        extract = []
        total = 0
        for (concept, quantity) in use.items():
            if isinstance(quantity, tuple):
                subtotal_list = []
                for child_quantity in quantity:
                    if concept.upper() in ["COMEDOR", "ATENCIÓN_TEMPRANA"] and child_quantity != 0:
                        subtotal_list.append(min(UNIT_PRICE[f'{concept}_MAX'],
                                                 child_quantity*UNIT_PRICE[concept]))
                subtotal = sum(subtotal_list)
                extract.append((concept.lower().replace('_', ' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))
            elif isinstance(quantity, int):
                if concept.upper() in ["COMEDOR", "ATENCIÓN_TEMPRANA"] and child_quantity != 0:
                    subtotal.append(min(UNIT_PRICE[f'{concept}_MAX'],
                                        child_quantity*UNIT_PRICE[concept]))
                subtotal = quantity*UNIT_PRICE[concept]
                extract.append((concept.lower().replace('_', ' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))

            elif isinstance(quantity, str):
                subtotal = int(quantity[:-1])
                extract.append((concept.lower().replace('_', ' '),
                                "",
                                "",
                                f"{subtotal:.2f} €"))

            if subtotal != 0:
                total += subtotal

        extract_tax = [(bold("Base Imponible"), "", "", bold(f"{total:.2f} €")),
                       (bold("IVA (exento)"), "", "", bold(f"{0:.2f} €")),
                       (bold("Total"), "", "", bold(f"{total:.2f} €"))]
        extract.extend(extract_tax)

        return extract

    def generate_additional_details(self):
        """
        Add details. For now, payment formula & IVA exemption.
        """
        with self.doc.create(Section('', numbering=False)):
            self.doc.append("FORMA DE PAGO: Domiciliación Bancaria\n")
            self.doc.append("Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")

    def generate_detailed_calendar(self):
        """
        Generate a calendar table with fields
        according to kids assistance.
        """
        child_attendance_matrices_dict = self.get_child_attendance_rows()

        calendar_tabu_spec = f'| X[2c] | {(7*"X[3c] | ")[:-1]}'
        with self.doc.create(LongTabu(calendar_tabu_spec,
                                      row_height=1.5)) as extract_table:
            extract_table.add_hline()
            extract_table.add_row(self.week_days_row,
                                  mapper=bold,
                                  color="black")

            for i, week in enumerate(self.matrix_rows_calendar):
                extract_table.add_hline()
                extract_table.add_row(week)
                extract_table.add_hline()
                for monthly_attendance in child_attendance_matrices_dict.values():
                    row = [dumps_list(cell) for cell in monthly_attendance[i]]
                    extract_table.add_row(row)
                extract_table.add_hline()
            extract_table.add_hline()

        with self.doc.create(LongTabu(" X[c] | X[7l] ",
                                      row_height=1)) as legend_table:
            for activity, color in ACTIVITIES_COLORS_DICT.items():
                legend_table.add_row([TextColor(color,
                                                'x'),
                                      activity])

        # self.doc.append(VerticalSpace('8ex'))

    def get_child_attendance_rows(self) -> dict:
        """
        Generate a dict of attendance.
        This method is a bit obscure in order to improve efficiency:
        for each kid, we want to generate a monthly row (see monthdayscalendar)
        attendance TeX object.

        Returns:
            dict: dict with childs as keys and
            values a list of len num days of month
            where each value is a concatenation of
            assistance colored characters.
        """
        E = [np.reshape(np.array(list(chain(self.initial_skip_list,
                                            [list(map(TextColor,
                                                      *(self.assigned_colors, daily_attendance)))
                                             for daily_attendance in zip(*activities_dict.values())],
                                            self.final_month_skip_list)),
                                 dtype=object),
                        (len(self.matrix_calendar), 7))
             for activities_dict in self.children_data.values()]

        attendance_rows_list = [np.concatenate((np.array([child]*len(self.matrix_calendar),
                                                         dtype="object")[:, None],
                                                monthly_attendance),
                                               axis=1)
                                for child, monthly_attendance in zip(self.children_data.keys(), E)]

        child_attendance_matrices_dict = dict(zip(self.children_data.keys(), attendance_rows_list))

        return child_attendance_matrices_dict

    def student_section(self,):
        with self.doc.create(Section('ALUMN@')):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                for field in ['Nombre',
                              'Apellidos',
                              'DNI',
                              'Fecha de nacimiento',
                              'Lugar de nacimiento',
                              'Numero de hermanos',
                              'Lugar que ocupa',
                              'Domicilio',
                              'Nacionalidad']:
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments=f'{field}: ',))
    def parents_section(self):
        for parent in ['MADRE/TUTORA',
                       'PADRE/TUTOR']:
            with self.doc.create(Section(parent)):
                with self.doc.create(Form()):
                    self.doc.append(Command('noindent'))
                    for field in ['Nombre',
                                  'Apellidos',
                                  'DNI',
                                  'Estudios',
                                  'Profesión',
                                  'Teléfono(s)',
                                  'Correo electrónico',
                                  'Domicilio']:
                        self.doc.append(Command('TextField',
                                                options=[NoEscape("width=\linewidth"),
                                                         "height=1in"],
                                                arguments=f'{field}: ',))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Firma y fecha: '))

    def LOPD_section(self):
        section_name = "CLÁUSULA DE PROTECCIÓN DE DATOS DE CARÁCTER PERSONAL"
        with self.doc.create(Section(section_name)):
            self.doc.append(CLAUSULA_PROT_DATOS)
            with self.doc.create(Subsection('ACEPTO: ')):
                self.doc.append(CLAUSULA_PROT_DATOS_PERSONAL)
                with self.doc.create(Form()):
                    arg1 = "como titular o representante legal del mismo, "
                    "consiente de forma inequívoca la presente cláusula "
                    "y política de privacidad de protección de datos de carácter personal:"
                    self.doc.append(Command('noindent'))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=10cm"),
                                                     "height=1in"],
                                            arguments='D/Dª',))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=10cm"),
                                                     "height=1in"],
                                            arguments=', con NIF o pasaporte Nº',))
                    self.doc.append(arg1)
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Firma y fecha: '))

    def LOPD_coop_section(self,):
        section_name = "Protección de Datos de Carácter Personal, Secreto y Confidencialidad"
        with self.doc.create(Section(section_name)):
            subsection_name = "Protección de Datos de Carácter Personal"
            with self.doc.create(Subsection(subsection_name)):
                self.doc.append(LOPD_COOP)
            subsection_name = "Deber de secreto y confidencialidad "
            with self.doc.create(Subsection(subsection_name)):
                self.doc.append(CONFIDENCIALIDAD)
            subsection_name = "Política de Protección de Datos"
            with self.doc.create(Subsection(subsection_name)):
                self.doc.append(POL_PROT_DATOS)
            with self.doc.create(Form()):
                    self.doc.append(Command('noindent'))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Firma y fecha: '))
            
    def image_posting_table(self):
        with self.doc.create(Tabular('| l | 4l |',
                                     row_height=1.2)) as associate_table:
            associate_table.addhline()
            associate_table.add_row(['',
                                     'NOMBRE, APELLIDOS Y DNI'])
            associate_table.add_row([bold("MENOR:"), 
                                     Command('TextField',
                                             options=[NoEscape("width=\linewidth"),
                                                      "height=1in"],
                                             arguments='Firma y fecha: ')])
            associate_table.add_hline()
            associate_table.add_row([bold("MENOR:"), 
                                     Command('TextField',
                                             options=[NoEscape("width=\linewidth"),
                                                      "height=1in"],
                                             arguments='Firma y fecha: ')])
            associate_table.add_hline()
            associate_table.add_row([bold("MENOR:"), 
                                     Command('TextField',
                                             options=[NoEscape("width=\linewidth"),
                                                      "height=1in"],
                                             arguments='Firma y fecha: ')])
            associate_table.add_hline()
            associate_table.add_row([bold("MADRE/TUTORA:"), 
                                     Command('TextField',
                                             options=[NoEscape("width=\linewidth"),
                                                      "height=1in"],
                                             arguments='Firma y fecha: ')])
            associate_table.add_hline()
            associate_table.add_row([bold("PADRE/TUTOR:"), 
                                     Command('TextField',
                                             options=[NoEscape("width=\linewidth"),
                                                      "height=1in"],
                                             arguments='Firma y fecha: ')])
            associate_table.add_hline()

    def image_posting_LOPD(self):
        self.doc.append(FootnoteText(PUB_IMAG))
        section_name = "Según lo expuesto, solicitamos tu consentimiento expreso para:"
        with self.doc.create(Section(section_name)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                arg1 = "La captación de imágenes y/o voz, vuestros, para su posterior difusión conforme lo "
                "descrito en la presente cláusula."
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=1ex"),"height=1ex"],
                                        arguments=arg1))
                arg2 = "La captación de imágenes y/o voz, del/de los menor/es "
                "(en tu condición de padre/madre/tutor legal) "
                "para su posterior difusión conforme lo descrito "
                "en la presente cláusula."
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=1ex"),
                                                 "height=1ex"],
                                        arguments=arg1))
                with self.doc.create(Form()):
                    self.doc.append(Command('noindent'))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Fecha: '))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Firma Madre/tutora y DNI: '))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Firma Padre/tutor y DNI: '))
                    self.doc.append(Command('TextField',
                                            options=[NoEscape("width=\linewidth"),
                                                     "height=1in"],
                                            arguments='Por el Colegio Andolina, firma y DNI: '))

    def parent_autorization(self):
        with self.doc.create(Form()):
            arg1 = "DOY MI AUTORIZACIÓN a cualquier excursión organizada o salida espontánea "
            "que surja de 9:30 a 14:00 de la mañana, "
            "a lo largo del presente curso y los sucesivos, salvo revocación expresa."
            arg2 = "Marcando esta casilla indico que no estoy de acuerdo "
            "con que se utilicen vehículos particulares "
            "para el transporte de mi hijo/a."
            self.doc.append(Command('noindent'))
            self.doc.append(Command('TextField',
                                    options=[NoEscape("width=10cm"),
                                             "height=1in"],
                                    arguments='D/Dª',))
            self.doc.append(Command('TextField',
                                    options=[NoEscape("width=10cm"),
                                             "height=1in"],
                                    arguments=', con NIF o pasaporte Nº',))
            self.doc.append(Command('ChoiceMenu',
                                    options=[NoEscape],
                                    arguments=['relación','madre,tutora legal,padre,tutor legal']))
            self.doc.append(arg1)
            self.doc.append(Command('Checkbox',
                                    options=[NoEscape("width=10cm"),
                                             "height=1in"],
                                    arguments=arg2))
            self.doc.append(Command('noindent'))
            self.doc.append(Command('TextField',
                                    options=[NoEscape("width=\linewidth"),
                                             "height=1in"],
                                    arguments='Firma y fecha: '))

    def health_info(self):
        with self.doc.create(Form()):
            self.doc.append(Command('noindent'))
            self.doc.append(Command('TextField',
                                    options=[NoEscape("width=\linewidth"),
                                             "height=1in"],
                                    arguments='Nombre del alumno: ',))
            self.doc.append(Command('TextField',
                                    options=[NoEscape("width=\linewidth"),
                                             "height=1in"],
                                    arguments='Fecha de nacimiento: ',))
        section = "ENFERMEDADES"
        arg1 = ["¿Tiene alguna enfermedad que requiera control médico o impida actividad física? ",
                "Sí=sí,No=no"]
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=10cm"),
                                                 "height=1in"],
                                        arguments=arg1))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='¿Cuál?: ',))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='Comentarios: ',))
        section = "ALERGIAS"
        arg1 = ["¿Tiene algún tipo de alergia a medicamentos, alimentos, animales, etc.? ",
                "Sí=sí,No=no"]
        arg2 = "En caso afirmativo, escriba sus manifestaciones: "
        arg3 = "La alergia se debe a: "
        arg4 = ["¿Recibe tratamiento permanente? ",
                "Sí=sí,No=no"]
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=10cm"),
                                                 "height=1in"],
                                        arguments=arg1))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments=arg2,))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments=arg3,))
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=10cm"),
                                                 "height=1in"],
                                        arguments=arg4))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='Comentarios: ',))
        section = "INTOLERANCIAS"
        arg1 = ["¿Tiene algún tipo de alergia a medicamentos, alimentos, animales, etc.? ",
                "Sí=sí,No=no"]
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=10cm"),
                                                 "height=1in"],
                                        arguments=arg1))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='Comentarios: ',))
        section = "VACUNAS"
        arg1 = ["¿Está vacunado del Tétanos? ",
                "Sí=sí,No=no"]
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('Checkbox',
                                        options=[NoEscape("width=10cm"),
                                                 "height=1in"],
                                        arguments=arg1))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='Comentarios: ',))
        section = "SI EL ALUMNO TIENE ALGÚN TIPO DE PROBLEMA DE SALUD EN EL COLEGIO RECURRIR A: "
        arg1 = "Institución-Médico y Teléfono: "
        arg2 = "Madre-Padre/Familiar y Teléfono: "
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments=arg1,))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments=arg2,))
        section = "INFORMACIÓN IMPORTANTE A DESTACAR: "
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('TextField',
                                        options=["name=multilinetextbox",
                                                 "multiline=true",
                                                 NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments="",))
        section = "FECHA Y FIRMA DE MADRE, PADRE O TUTOR, DNI: "
        with self.doc.create(Section(section)):
            with self.doc.create(Form()):
                self.doc.append(Command('noindent'))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='Firma y fecha: '))
                self.doc.append(Command('TextField',
                                        options=[NoEscape("width=\linewidth"),
                                                 "height=1in"],
                                        arguments='DNI: '))


@dataclass
class Person:
    fullname: str
    NIF: str
    adress: str

class AssociateType(Enum):
    """Different types of associates."""
    COLABORADOR = auto()
    SOCIO = auto()

@dataclass
class Associate(Person):
    """
    A class for associates
    """
    id: str = ''

@dataclass
class Student:
    """
    A class for students

    Args:
        name (str): First name of student
        associate (str): Legal representative, cooperative member
        attendance (dict): keys -> activities, values -> list[str]
            representing the attendance to activity
    """
    fullname: str
    associate: Associate
    attendance: list[dict]

@dataclass
class StudentsFamily:
    """
    A class for students linked to a single associate

    Args:
        associate (str): Legal representative, cooperative member
        children (list[Student]): List of Student represented by associate
    """
    associate: Associate
    children: list[Student]

@dataclass
class ChildInfo(Person):
    """Enrollment data
    """
    birthdate: str
    birthplace: str
    num_siblings: str
    position_siblings: str
    nationality: str
    NIF: str = ''

class LegalRelation(Enum):
    MADRE = auto()
    PADRE = auto()
    TUTORA_LEGAL = auto()
    TUTOR_LEGAL = auto()

@dataclass
class Parent(Person):
    """Associate, parent, legal tutor or legal representant of Andolina
    """
    signature: str
    relation_with_child: Literal['madre','padre','tutora legar','tutor legal','']
    education: str  # =''
    occupation: str # =''
    telephone: str  # =''
    email: str      # =''

@dataclass
class ImagePostingAuth:
    """Image posting authorization LOPD
    section_name = "Según lo expuesto, solicitamos tu consentimiento expreso para:"
    arg1 = "La captación de imágenes y/o voz, vuestros, para su posterior difusión conforme lo "
    "descrito en la presente cláusula."
    arg2 = "La captación de imágenes y/o voz, del/de los menor/es "
    "(en tu condición de padre/madre/tutor legal) "
    "para su posterior difusión conforme lo descrito "
    "en la presente cláusula."
    """
    tutor1: Parent
    tutor2: Parent
    auth_Andolina: Parent = Parent(*['']*9)
    date: str = field(default_factory=lambda: date.today().strftime('%Y-%m-%d'))

@dataclass
class OutingAuthorization(Parent):
    """School outing authorization.
    
    arg1 = "DOY MI AUTORIZACIÓN a cualquier excursión organizada o salida espontánea "
    "que surja de 9:30 a 14:00 de la mañana, "
    "a lo largo del presente curso y los sucesivos, salvo revocación expresa."
    arg2 = "Marcando esta casilla indico que no estoy de acuerdo "
    "con que se utilicen vehículos particulares "
    "para el transporte de mi hijo/a."
    """
    important_info: str = ''
    date: str = field(default_factory=lambda: date.today().strftime('%Y-%m-%d'))

    outing_permission: str = ''
    private_vehicle: str = ''

class Binario(Enum):
    SI = auto()
    NO = auto()
    
@dataclass
class HealthInfo(Parent):
    """Health info summary
    
    section = "ALERGIAS"
    arg1 = "¿Tiene algún tipo de alergia a medicamentos, alimentos, animales, etc.? "
    arg2 = "En caso afirmativo, escriba sus manifestaciones: "
    arg3 = "La alergia se debe a: "
    arg4 = "¿Recibe tratamiento permanente? "
    
    section = "INTOLERANCIAS"
    arg1 = "¿Tiene algún tipo de alergia a medicamentos, alimentos, animales, etc.? "
            
    section = "VACUNAS"
    arg1 = "¿Está vacunado del Tétanos? "
            
    section = "SI EL ALUMNO TIENE ALGÚN TIPO DE PROBLEMA DE SALUD EN EL COLEGIO RECURRIR A: "
    arg1 = "Institución-Médico y Teléfono: "
    arg2 = "Madre-Padre/Familiar y Teléfono: "
    section = "INFORMACIÓN IMPORTANTE A DESTACAR: "
    section = "FECHA Y FIRMA DE MADRE, PADRE O TUTOR, DNI: "
    """
    important_info_comments: str = ''
    date: str = field(default_factory=lambda: date.today().strftime('%Y-%m-%d'))
    
    allergies = Literal['sí','no']
    manifestations: str = ''
    trigger: str = ''
    treatment = Literal['sí','no']
    allergies_comments: str = ''
    
    intolerances = Literal['sí','no']
    intolerances_comments: str = ''
    
    vaccines = Literal['sí','no']
    vaccines_comments: str = ''
    
    pro_emergency_contact: list = field(default_factory=lambda: ['',''])
    fam_emergency_contact: list = field(default_factory=lambda: ['',''])


    