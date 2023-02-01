'''
Generate pdf files with pylatex
for invoices or detailed extracts.
'''
# import stdlib
from datetime import date
from dataclasses import dataclass

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
from .LaTeX_snippets import Billing, PdfGen
from .data_types import Person

# Constants
from .constants import (
    COLEGIO_DATOS,
    EXEMPTION,
    LOPD,
    PAYMENT_METHOD,
    UNIT_PRICE,
)



@dataclass
class MonthlyInvoice:
    month: str
    # year: str
    month_quantities: dict

class Invoice(PdfGen,Billing):
    def __init__(self,
                 associate: Person,
                 associate_extract: list[MonthlyInvoice],
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
        self.associate_extract = associate_extract

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
        for month_data in self.associate_extract:
            self.generate_invoice_id()
            self.generate_invoice(month_data)
        filename = f"{self.associate.name}-{self.invoice_num}"
        self.generate_file(filename)

    def generate_invoice(self,
                         month_data: dict):
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

        self.generate_invoice_table(month_data)

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


    def generate_invoice_table(self, month_data):
        """
        Generate a table with the extract for current invoice
        """
        with self.doc.create(Section(f'Factura {month_data.month}',numbering=False)):
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

            extract_final = generate_extract(month_data.month_quantities)
            for row in extract_final:
                invoice_table.add_hline()
                invoice_table.add_row(row)

            self.doc.append(VerticalSpace('2ex'))

    def additional_details(self):
        self.doc.append(PAYMENT_METHOD)
        self.doc.append(NewLine())
        self.doc.append(EXEMPTION)


def generate_extract(month_quantities: dict) -> list[tuple]:
    """
    Generate current extract data into a list of rows (tuples).
    
    Args:
        month_quantities (MonthlyQuantity): instance where fields are concepts (keys of UNIT_PRICE)
        and values are the quantities used in a given month by a child.

    Returns:
        list[tuple]: list of rows in extract
    """
    extract = []
    total = 0.
    for concept,quantity in month_quantities.items():
        # concept depending on attendance, such as lunch or early atention
        if isinstance(quantity,tuple):
            subtotal = min(len(quantity)*UNIT_PRICE[concept],
                           UNIT_PRICE[f'{concept}_MAX'])
            extract.append((concept.lower().replace('_', ' '),
                            f"{UNIT_PRICE[concept]:.2f} €",
                            f"{quantity}",
                            f"{subtotal:.2f} €"))
        # monthly paid activities, such as judo
        elif isinstance(quantity,int):
            subtotal = quantity*UNIT_PRICE[concept]
            extract.append((concept.lower().replace('_', ' '),
                            f"{UNIT_PRICE[concept]:.2f} €",
                            f"{quantity}",
                            f"{subtotal:.2f} €"))
        # Exceptional payment, such as accompaniment or course
        elif isinstance(quantity, float):
            subtotal = quantity
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
                       [MonthlyInvoice(month=11,
                                       month_quantities=dict(zip(concepts,
                                                                 ((2,),(3,),1,0,0,0,1,2.,51.,0.,0.))))])
    
    instance.generate_set_invoices()

    