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
import locale
from typing import Literal, Optional
import os

# import external libs
import numpy as np
from pylatex import (Command, Document, Foot, FootnoteText, Head, HugeText, LargeText, LineBreak,
                     LongTabu, MiniPage, NoEscape, Package, PageStyle, Section, StandAloneGraphic, Subsection,
                     Tabular, VerticalSpace, TextColor)
from pylatex.utils import NoEscape, bold, dumps_list
from pylatex.base_classes import Environment

# import self API
from data_types import Associate, Student
from LaTeX_snippets import TeXfile

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


@dataclass
class MonthlyAttendanceCalendar:
    dining_attendance: tuple(bool)
    early_attendance: tuple(bool)
    num_quotas: tuple(bool)
    judo_quotas: tuple(bool)
    ciencia_quotas: tuple(bool)
    teatro_quotas: tuple(bool)
    robotix_quotas: tuple(bool)
    accompaniment: tuple(bool)
    trainings: tuple(bool)
    workshops: tuple(bool)
    camps: tuple(bool)

@dataclass
class StudentMonthlyAttendance:
    student: Student
    monthly_attendance: MonthlyAttendanceCalendar


class Extract(TeXfile):
    def __init__(self,
                 associate: Associate,
                 student_attendance: list[StudentMonthlyAttendance],
                 series: str = 'FU',
                 invoice_num_start: int = 0,
                 associate_data: list[dict] = [{'name': 'Ejemplo Ejemplez'}],
                 child_data: list[dict] = [{}]) -> None:
        """This class generates different kinds of pdf documents using pylatex

        Args:
            series (str, optional): invoice series. Defaults to 'FU'.
            invoice_num_start (int, optional): invoice number to start with.
                                               Defaults to 0.
            associate_data (list[dict], optional): each dict represents
                an associate.
                Migrating to dataclass.
                Defaults to [{'name': 'Ejemplo Ejemplez'}].
            child_data (list[dict], optional): each element corresponds to a
                dict with the children represented by a single associate.
                The dict has the children as keys and the values
                are dicts activities - attendance.
                Migrating to dataclass. Defaults to [{}].
        """

        # basic file data
        self.series = series
        self.invoice_num_start = invoice_num_start
        self.current_invoice_num = invoice_num_start
        self.associates_data = associate_data
        self.childs_data = child_data

        # dates
        self.invoice_date = date.today()
        self.year = self.invoice_date.year
        self.month = self.invoice_date.month
        current_year_formated = self.year % 100
        self.current_academic_year = (f"{current_year_formated}"
                                      f"{current_year_formated + 1}")

        # extract data
        self.initial_skip, self.num_monthdays = calendar.monthrange(self.year,
                                                                    self.month)
        cal = calendar.Calendar()
        self.matrix_calendar = [[x if x != 0 else ''
                                 for x in week]
                                for week in cal.monthdayscalendar(self.year,
                                                                  self.month)]
        self.matrix_rows_calendar = np.concatenate((np.array([''] * len(self.matrix_calendar),
                                                             dtype="object")[:, None],
                                                    self.matrix_calendar),
                                                   axis=1)
        self.final_month_skip = 7 * len(self.matrix_calendar) - (self.initial_skip + self.num_monthdays)
        self.initial_skip_list = [''] * self.initial_skip
        self.final_month_skip_list = [''] * self.final_month_skip
        locale.setlocale(locale.LC_TIME,
                         'es_ES.UTF-8')
        self.week_days = list(calendar.day_name)
        self.week_days_row = list(chain([''],
                                        self.week_days))
        self.assigned_colors = [ACTIVITIES_COLORS_DICT[activity.upper()]
                                for activity in ACTIVIDADES]

    def generate_all_detailed_extracts(self):
        """
        Generate a lis of detailed extracts
        """
        for associate in self.associates_data:
            self.generate_single_detailed_extract(associate_data=associate,
                                                  kids_data=self.childs_data[associate['name']])

    def generate_single_detailed_extract(self,
                                         associate_data,
                                         kids_data):
        """Generate a detailed extract with a calendar and
        legend for each child assistance to every activity.

        Args:
            associate_data (_type_): the data of an associate
            kids_data (_type_): the dict of kids with values
                dict activities - attendance.
        """
        self.current_associate_data = associate_data
        self.current_child_data = kids_data

        self.mode = 'extract'
        self.generate_header()
        self.generate_footer()
        self.generate_associate_table()
        self.doc.preamble.append(self.first_page)

        self.generate_detailed_calendar()

        self.generate_file(mode='extract')

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
             for activities_dict in child_data.values()]

        attendance_rows_list = [np.concatenate((np.array([child]*len(self.matrix_calendar),
                                                         dtype="object")[:, None],
                                                monthly_attendance),
                                               axis=1)
                                for child, monthly_attendance in zip(child_data.keys(), E)]

        child_attendance_matrices_dict = dict(zip(child_data.keys(), attendance_rows_list))

        return child_attendance_matrices_dict

    def generate_set_invoices(self):
        for associate_data in self.associates_data:
            self.generate_invoice(associate_data)

    def generate_invoice(self,
                         associate_data):
        """Generate invoice from associate data.

        Args:
            associate_data (_type_): Generate an invoice for current associate.
        """
        self.current_associate_data = associate_data

        self.mode = 'invoice'
        self.generate_header()
        self.generate_footer()
        self.generate_associate_table()
        self.doc.preamble.append(self.first_page)

        self.generate_invoice_table()

        self.generate_additional_details()

        self.generate_file(mode='invoice')

    def generate_header(self):
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

        self.generate_invoice_id()
        # Add document title
        with self.first_page.create(Head("R")) as right_header:
            with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                              pos='c', align='l')) as title_wrapper:
                title_wrapper.append(LargeText(bold(f"Número de factura: {self.current_associate_data['invoice_num']}")))
                title_wrapper.append(LineBreak())
                title_wrapper.append(LineBreak())
                title_wrapper.append(TextColor('black',
                                               LargeText(bold(f"Fecha: {self.current_associate_data['date']}"))))

        self.doc.append(VerticalSpace('8ex'))

    def generate_invoice_id(self) -> str:
        '''
        Get current invoice number formated
        Example: FU-2223-001
        '''
        self.current_associate_data['invoice_num'] = f'{self.series}-{self.current_academic_year}-{self.current_invoice_num:03}'
        self.current_invoice_num += 1
        self.current_associate_data['date'] = self.invoice_date.strftime("%d/%m/%y")

    def generate_footer(self):
        """
        Generate footer. For the time being, with LOPD & School adress
        """
        with self.first_page.create(Foot("L")) as footer:
            footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))

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

    def generate_additional_details(self):
        """
        Add details. For now, payment formula & IVA exemption.
        """
        with self.doc.create(Section('', numbering=False)):
            self.doc.append("FORMA DE PAGO: Domiciliación Bancaria\n")
            self.doc.append("Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")

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


@dataclass
class Associate:
    """
    A class for associates
    """
    name: str
    NIF: str
    adress: str
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
    name: str
    associate: str
    attendance: list[dict]


@dataclass
class Children:
    """
    A class for students

    Args:
        associate (str): Legal representative, cooperative member
        children (list[Student]): List of Student represented by associate
    """
    associate: Associate
    children: list[Student]


if __name__ == '__main__':
    # invoice_date = date.today()
    data = {  # 'invoice_num': get_invoice_num(invoice_date),
              # 'date': invoice_date.strftime("%d/%m/%y"),
            'name': 'Ejemplo Ejemplez Ejemplez',
            'NIF': '123456789B',
            'adress': 'C/ Dirección. Código Postal, Localidad, Provincia'}

    # generate_invoice(**data)
    instance = Extract(invoice_num_start=2,
                             associate_data=[data, data])
    from random import choices
    child_data = {
        'Asier': dict(zip(ACTIVIDADES, [choices(['x', ''],
                                                k=instance.num_monthdays)
                                        for act in ACTIVIDADES])),
        'Mike': dict(zip(ACTIVIDADES, [choices(['x', ''],
                                               k=instance.num_monthdays)
                                       for act in ACTIVIDADES])),
    }
    instance.childs_data = child_data

    instance.generate_set_invoices()
    instance.generate_single_detailed_extract(data,
                                              child_data)


    