'''
Generate pdf files with pylatex
for invoices or detailed extracts.
'''
# import stdlib
import calendar
import csv
from dataclasses import dataclass
from enum import Enum, auto
from itertools import chain
from os import path
from typing import Dict

# import external libs
from pylatex import (
    FootnoteText,
    Head,
    LargeText,
    LineBreak,
    LongTabu,
    NewLine,
    NewPage,
    PageStyle,
    Section,
    VerticalSpace,
    TextColor
    )
from pylatex.utils import bold

# import self API
from LaTeX_snippets import Billing, PdfGen
from data_types import Person

# Constants
from constants import (
    COLEGIO_DATOS,
    EXEMPTION,
    LOPD,
    PAYMENT_METHOD,
    UNIT_PRICE,
)

class ActivityPayment(Enum):
    monthly = auto()
    monthly_max = auto()
    daily = auto()

@dataclass
class BillableActivity:
    name: str
    participation: tuple[int]
    payment: ActivityPayment
    price: float
    max_price: float=0

    def __post_init__(self):
        self.quantity = len(self.participation)

    def compute_activity_cost(self) -> float:
        # concept depending on attendance, such as lunch or early atention
        if self.payment == ActivityPayment.monthly_max:
            cost = min(self.price * self.quantity,
                       self.max_price)

        # monthly paid activities, such as judo
        if self.payment == ActivityPayment.monthly:
            cost = self.price * self.quantity

        # Exceptional payment, such as accompaniment or course
        elif isinstance(self.quantity, float):
            cost = self.quantity

        return cost


@dataclass
class MonthBillableData:
    invoice_date: str
    invoice_num: int
    month: int
    academic_year: str
    billable_activities: tuple[BillableActivity]
    series: str='FU'

    def __post_init__(self):
        self.invoice_id = f'{self.series}-{self.academic_year}-{self.invoice_num}'
        # self.full_month = f'{self.month}{self.academic_year}'
        # cal = calendar.Calendar()
        # locale.setlocale(locale.LC_TIME,
        #                  'es_ES.UTF-8')
        self.month_name = calendar.month_name[self.month]

    def generate_extract(self) -> tuple[tuple[str,str,str,str]]:
        costs = self.compute_cost_tuple()
        
        extract = tuple(((billable_activity.name,
                    f"{billable_activity.price:.2f} €",
                    f"{billable_activity.quantity}",
                    f"{cost:.2f} €") 
                    for (billable_activity,cost) in zip(self.billable_activities,costs)))

        total = sum(costs)
        extract_tax = ((bold("Base Imponible"), "", "", bold(f"{total:.2f} €")),
                       (bold("IVA (exento)"), "", "", bold(f"{0:.2f} €")),
                       (bold("Total"), "", "", bold(f"{total:.2f} €")))

        return chain(extract, extract_tax)

    def compute_cost_tuple(self) -> tuple[float]:
        return (billable_activity.compute_activity_cost() for billable_activity in self.billable_activities)

@dataclass
class Remittance:
    month: str
    academic_year: str
    month_billable_data_dict: Dict[Person,MonthBillableData]
    
    def __post_init__(self):
        self.full_month = f'{self.month}{self.academic_year}'
        self.person_cost_tuple = ((person.name,sum(month_billable_data.compute_cost_tuple)) for 
                                  (person,month_billable_data) in self.month_billable_data_dict.items())

    def to_csv(self):
        filepath = f'remittance_{self.full_month}.csv'
        with open(file=filepath,
                  mode='w',
                  newline='') as f:
            writer = csv.writer(f, 
                                delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            (writer.writerow(person_cost) for person_cost in self.person_cost_tuple)
        return filepath


class Invoice(PdfGen,Billing):
    def __init__(self,
                 associate: Person,
                 associate_extract: MonthBillableData) -> None:
        """This class generates different kinds of pdf documents using pylatex

        Args:
            series (str, optional): invoice series. Defaults to 'FU'.
            invoice_num_start (int, optional): invoice number to start with.
                                               Defaults to 0.
            associate_data (tuple[dict], optional): each dict represents
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
        self.associate = associate
        self.associate_extract = associate_extract

        # dates
        # self.year = self.associate_extract.invoice_date.year
        # self.month = self.associate_extract.invoice_date.month
        # current_year_formated = self.year % 100
        # self.current_academic_year = (f"{current_year_formated}"
        #                               f"{current_year_formated + 1}")

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

    def to_pdf(self):
        self.generate_invoice()
        filename = f"{self.associate.name}-{self.associate_extract.invoice_id}"
        self.generate_file(filename)

    def generate_invoice(self):
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
        super().generate_associate_table(self.associate)

        self.generate_invoice_table()

        self.generate_additional_details()
        
        self.doc.append(NewPage())
        
        
    def document_title(self, title_wrapper: Head("R")) -> None:
        title_wrapper.append(LargeText(bold(f"Número de factura: {self.associate_extract.invoice_id}")))
        title_wrapper.append(LineBreak())
        title_wrapper.append(LineBreak())
        title_wrapper.append(TextColor('black',
                                        LargeText(bold(f"Fecha: {self.associate_extract.invoice_date}"))))

    def footer(self, footer):
        """
        Generate footer. For the time being, with LOPD & School adress
        """
        footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))

    def generate_invoice_table(self):
        """
        Generate a table with the extract for current invoice
        """
        with self.doc.create(Section(f'Factura {self.associate_extract.month_name}',numbering=False)):
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

            extract_final = self.associate_extract.generate_extract()
            for row in extract_final:
                invoice_table.add_hline()
                invoice_table.add_row(row)

            self.doc.append(VerticalSpace('2ex'))

    def additional_details(self):
        self.doc.append(PAYMENT_METHOD)
        self.doc.append(NewLine())
        self.doc.append(EXEMPTION)


if __name__ == '__main__':
    concepts = ['COMEDOR',
                'ATENCIÓN_TEMPRANA',
                'CUOTA',
                'JUDO',
                'CIENCIA',
                'TEATRO',
                'ROBOTIX',
                'accompaniment',
                'trainings',
                'workshops',
                'camps',]
    instance = Invoice(Person('mike','ex','123'),
                       MonthBillableData(invoice_date='11-22',
                                          invoice_num=1,
                                          month=11,
                                          academic_year='2223',
                                          billable_activities=(
                                              BillableActivity(name='cuota mensual hijo1',
                                                               participation=(1,2,3),
                                                               payment=ActivityPayment.monthly,
                                                               price=325,),
                                              BillableActivity(name='atencion temprana',
                                                               participation=(1,2,3),
                                                               payment=ActivityPayment.monthly_max,
                                                               price=1,
                                                               max_price=15),
                                              
                                          )))
    
    instance.to_pdf()

    