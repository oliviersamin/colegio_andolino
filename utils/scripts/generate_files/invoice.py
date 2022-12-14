'''
Generate pdf files with pylatex
for invoices or detailed extracts.
'''
# import stdlib
import calendar
from datetime import date
from dataclasses import dataclass, fields
from enum import Enum, auto
from itertools import chain
import locale
from typing import Literal, Optional
import os

# import external libs
import numpy as np
from pylatex import (Command, Document, Foot, FootnoteText, Head, HugeText, LargeText, LineBreak,
                     LongTabu, MiniPage, NewPage, NoEscape, Package, PageStyle, Section, StandAloneGraphic, Subsection,
                     Tabular, VerticalSpace, TextColor)
from pylatex.utils import NoEscape, bold, dumps_list
from pylatex.base_classes import Environment

# import self API
from data_types import Associate, Student
from LaTeX_snippets import Billing, PdfGen

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
class MonthlyQuantity:
    COMEDOR: tuple[int]
    ATENCIÓN_TEMPRANA: tuple[int]
    CUOTA: int
    JUDO: int
    CIENCIA: int
    TEATRO: int
    ROBOTIX: int
    # dining_attendance: tuple[int]
    # early_attendance: tuple[int]
    # num_quotas: int
    # judo_quotas: int
    # ciencia_quotas: int
    # teatro_quotas: int
    # robotix_quotas: int
    accompaniment: float
    trainings: float
    workshops: float
    camps: float

@dataclass
class MonthlyInvoice:
    month: str
    # year: str
    monthly_quantities: MonthlyQuantity


class Invoice(PdfGen,Billing):
    def __init__(self,
                 associate: Associate,
                 associate_period: list[MonthlyInvoice],
                 series: str = 'FU',
                 invoice_num_start: int = 0) -> None:
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
        super().__init__()
        # basic file data
        self.series = series
        self.invoice_num_start = invoice_num_start
        self.current_invoice_num = invoice_num_start
        self.associate = associate
        self.associate_period = associate_period

        # dates
        self.invoice_date = date.today()
        self.year = self.invoice_date.year
        self.month = self.invoice_date.month
        current_year_formated = self.year % 100
        self.current_academic_year = (f"{current_year_formated}"
                                      f"{current_year_formated + 1}")

        # # extract data
        # self.initial_skip, self.num_monthdays = calendar.monthrange(self.year,
        #                                                             self.month)
        # cal = calendar.Calendar()
        # self.matrix_calendar = [[x if x != 0 else ''
        #                          for x in week]
        #                         for week in cal.monthdayscalendar(self.year,
        #                                                           self.month)]
        # self.matrix_rows_calendar = np.concatenate((np.array([''] * len(self.matrix_calendar),
        #                                                      dtype="object")[:, None],
        #                                             self.matrix_calendar),
        #                                            axis=1)
        # self.final_month_skip = 7 * len(self.matrix_calendar) - (self.initial_skip + self.num_monthdays)
        # self.initial_skip_list = [''] * self.initial_skip
        # self.final_month_skip_list = [''] * self.final_month_skip
        # locale.setlocale(locale.LC_TIME,
        #                  'es_ES.UTF-8')
        # self.week_days = list(calendar.day_name)
        # self.week_days_row = list(chain([''],
        #                                 self.week_days))
        # self.assigned_colors = [ACTIVITIES_COLORS_DICT[activity.upper()]
        #                         for activity in ACTIVIDADES]

    def generate_set_invoices(self):
        for month in self.associate_period:
            self.generate_invoice_id()
            self.generate_invoice(month)
        filename = f"{self.associate.name}-{self.invoice_num}"
        self.generate_file(filename)

    def generate_invoice(self,
                         month: MonthlyInvoice):
        """Generate invoice from associate data.

        Args:
            associate_data (_type_): Generate an invoice for current associate.
        """
        # self.mode = 'invoice'
        page = PageStyle('page')
        self.doc.change_page_style(page.name)
        self.doc.preamble.append(page)
        super().add_header(page)
        super().add_footer(page)

        # unique of this class
        super().generate_associate_table(self.associate.name,self.associate.NIF,self.associate.adress)

        self.generate_invoice_table(month)

        self.generate_additional_details()
        
        self.doc.append(NewPage())
        
        
    def document_title(self, title_wrapper: Head("R")) -> None:
        title_wrapper.append(LargeText(bold(f"Número de factura: {self.invoice_num}")))
        title_wrapper.append(LineBreak())
        title_wrapper.append(LineBreak())
        title_wrapper.append(TextColor('black',
                                        LargeText(bold(f"Fecha: {self.date}"))))

    def footer(self, footer):
        """
        Generate footer. For the time being, with LOPD & School adress
        """
        footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))

    def generate_invoice_id(self) -> str:
        '''
        Get current invoice number formated
        Example: FU-2223-001
        '''
        self.invoice_num = f'{self.series}-{self.current_academic_year}-{self.current_invoice_num:03}'
        self.current_invoice_num += 1
        self.date = self.invoice_date.strftime("%d/%m/%y")


    def generate_invoice_table(self, monthly_data):
        """
        Generate a table with the extract for current invoice
        """
        with self.doc.create(Section(f'Factura {monthly_data.month}',numbering=False)):
            ...

        with self.doc.create(LongTabu("X[3l] X[c] X[c] X[c]",
                                      row_height=1.5)) as invoice_table:
            invoice_table.add_row(["concepto",
                                   "precio unitario",
                                   "cantidad",
                                   "subtotal"],
                                  mapper=bold,
                                  color="lightgray")
            invoice_table.add_empty_row()

            extract_final = self.generate_extract(monthly_data.monthly_quantities)
            for row in extract_final:
                invoice_table.add_hline()
                invoice_table.add_row(row)

            self.doc.append(VerticalSpace('2ex'))

    def generate_extract(self, monthly_quantities: MonthlyQuantity) -> list[tuple]:
        """
        Generate current extract data into a list of rows (tuples).
        
        Args:
            monthly_quantities (MonthlyQuantity): instance where fields are concepts (keys of UNIT_PRICE)
            and values are the quantities used in a given month by a child.

        Returns:
            list[tuple]: list of rows in extract
        """
        extract = []
        total = 0.
        for field in fields(monthly_quantities):
            concept = field.name
            quantity = getattr(monthly_quantities,
                               concept)
            if isinstance(quantity,tuple):
                subtotal_list = [0.,]
                for child_quantity in quantity:
                    if concept.upper() in ["COMEDOR", "ATENCIÓN_TEMPRANA"]:
                        subtotal_list.append(min(UNIT_PRICE[f'{concept}_MAX'],
                                                 child_quantity*UNIT_PRICE[concept]))
                subtotal = sum(subtotal_list)
                extract.append((concept.lower().replace('_', ' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))
            elif isinstance(quantity,int):
                subtotal = quantity*UNIT_PRICE[concept]
                extract.append((concept.lower().replace('_', ' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))
            elif isinstance(quantity, float):
                extract.append((concept.lower().replace('_', ' '),
                                "",
                                "",
                                f"{quantity:.2f} €"))
        
            total += subtotal

        extract_tax = [(bold("Base Imponible"), "", "", bold(f"{total:.2f} €")),
                       (bold("IVA (exento)"), "", "", bold(f"{0:.2f} €")),
                       (bold("Total"), "", "", bold(f"{total:.2f} €"))]
        extract.extend(extract_tax)

        return extract

    def additional_details(self):
        self.doc.append("FORMA DE PAGO: Domiciliación Bancaria\n")
        self.doc.append("Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")



if __name__ == '__main__':
    # invoice_date = date.today()
    data = {  # 'invoice_num': get_invoice_num(invoice_date),
              # 'date': invoice_date.strftime("%d/%m/%y"),
            'name': 'Ejemplo Ejemplez Ejemplez',
            'NIF': '123456789B',
            'adress': 'C/ Dirección. Código Postal, Localidad, Provincia'}

    # generate_invoice(**data)
    instance = Invoice(Associate('mike','ex','123','socio'),
            [MonthlyInvoice(11,
                            MonthlyQuantity((2,),(3,),1,0,0,0,1,2.,51.,0.,0.))])
    

    instance.generate_set_invoices()

    