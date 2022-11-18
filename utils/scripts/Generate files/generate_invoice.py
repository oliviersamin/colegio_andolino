'''
Generate invoice
'''
import calendar
from datetime import date
from dataclasses import dataclass
from itertools import chain
from functools import partial
from json import dumps as jdumps
from json import loads as jloads
import locale
import os

from pylatex import (Document, Foot, FootnoteText, Head, LargeText, LineBreak,
                     LongTabu, MiniPage, PageStyle, Section, StandAloneGraphic,
                     Tabular, VerticalSpace, TextColor)
# from pylatex import MultiColumn, Tabu, NewLine, Tabularx,
# from pylatex import TextColor, simple_page_number, SmallText, LongTable
from pylatex.utils import NoEscape, bold, dumps_list
import numpy as np

###########################################################################
########################## ENVIRONMENT VARIABLES ##########################
###########################################################################

############################# Billing concepts ############################
PRECIO_MAX_COMEDOR = int(os.getenv('PRECIO_MAX_COMEDOR', '20'))
PRECIO_DIA_COMEDOR = int(os.getenv('PRECIO_DIA_COMEDOR', '5'))
PRECIO_MAX_TEMPRANA = int(os.getenv('PRECIO_MAX_TEMPRANA', '20'))
PRECIO_DIA_TEMPRANA = int(os.getenv('PRECIO_DIA_TEMPRANA', '5'))
EXTRAESCOLARES = jloads(os.getenv('EXTRAESCOLARES',
                                 '{"JUDO": 25, "CIENCIA": 20, "TEATRO": 20, "ROBOTIX": 20}'))
ACTIVIDADES_ESCOLARES = ['COLEGIO', 'ATENCIÓN TEMPRANA', 'COMEDOR']
ACTIVIDADES = ACTIVIDADES_ESCOLARES
ACTIVIDADES.extend(EXTRAESCOLARES.keys())
UNIT_PRICES_DICT = {"CUOTA": 325,
                    "COMEDOR": 5,
                    "COMEDOR_MAX": 25,
                    "ATENCIÓN_TEMPRANA": 5,
                    "ATENCIÓN_TEMPRANA_MAX": 25,
                    "JUDO": 25,
                    "CIENCIA": 20,
                    "TEATRO": 20,
                    "ROBOTIX": 20}
UNIT_PRICE = jloads(os.getenv('UNIT_PRICE',
                              jdumps(UNIT_PRICES_DICT)))

########################### Information Strings ###########################
COLEGIO_NOMBRE = os.getenv("COLEGIO_NOMBRE",
                           "Colegio Andolina Sociedad Cooperativa Asturiana")
COLEGIO_CIF = os.getenv("COLEGIO_NOMBRE",
                        "F33986522")
COLEGIO_DIRECCION = os.getenv("COLEGIO_DIRECCION",
                              "Camino del Barreo, 203 Cefontes (Cabueñes) 33394 Gijón Asturias.")
COLEGIO_DATOS = os.getenv("COLEGIO_DATOS",
                          f'{COLEGIO_NOMBRE} - CIF: {COLEGIO_CIF} - {COLEGIO_DIRECCION}')
EXEMPTION = os.getenv("EXEMPTION",
                      "Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")
LOPD = os.getenv("LOPD",
                 "A los efectos previstos en la Ley Orgánica 15/1999, de 13 de diciembre, " +
                 "sobre Protección de Datos de Carácter Personal, se le informa que los " +
                 "datos personales proporcionados se incorporarán a los ficheros de " +
                 "Colegio Andolina Sociedad Cooperativa Asturiana, " +
                 f"con dirección en {COLEGIO_DIRECCION} " +
                 "La finalidad del tratamiento de los datos será " +
                 "la de gestionar los servicios suministrados. " +
                 "Usted tiene derecho al acceso, rectificación, cancelación y " +
                 "oposición en los términos previstos en la Ley, " +
                 "que podrá ejercitar mediante escrito " +
                 "dirigido al responsable de los mismos en la dirección anteriormente indicada " +
                 "o a la dirección de correo electrónico lopd@colegioandolina.org.")


COLORS = ["black", "blue", "brown", "cyan", "darkgray", "gray",
          "green", "lightgray", "lime", "magenta", "olive", "orange",
          "pink", "purple", "red", "teal", "violet", "white", "yellow"]
assign_colors = dict(zip(ACTIVIDADES,COLORS))

class PdfGeneration():

    def __init__(self, 
                 series: str='FU',
                 invoice_num_start: int=0,
                 associate_data: list[dict]=[{'name': 'Ejemplo Ejemplez'}],
                 child_data: list[dict]=[{}]) -> None:
        """
        This class generates different kinds of pdf documents using pylatex

        Args:
            mode (str, optional): invoice, details. Defaults to 'invoice'.
        """
        ###################################################################################
        ############################ Document Geometry Options ############################
        ###################################################################################
        self.geometry_options = {
            "head": "40pt",
            "margin": "0.5in",
            "bottom": "1.6in",
            "includeheadfoot": True
        }

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
        current_year_formated = self.year%100
        self.current_academic_year = f"{current_year_formated}{current_year_formated+1}"

        # extract data
        self.initial_month_skip, self.num_monthdays = calendar.monthrange(self.year,self.month)
        self.current_calendar = calendar.Calendar()
        self.matrix_calendar = [[x if x != 0 else '' for x in week] for week in self.current_calendar.monthdayscalendar(self.year, self.month)]
        self.matrix_rows_calendar = np.concatenate((np.array(['']*len(self.matrix_calendar))[:,None],
                                                    self.matrix_calendar),
                                                   axis=1)
        self.final_month_skip = 7*len(self.matrix_calendar) - (self.initial_month_skip + self.num_monthdays)
        self.initial_month_skip_list = ['']*self.initial_month_skip
        self.final_month_skip_list = ['']*self.final_month_skip
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.week_days = list(calendar.day_name)
        self.week_days_row = list(chain([''],self.week_days))
        self.assigned_colors = [assign_colors[activity.upper()] for activity in ACTIVIDADES]


    def generate_set_detailed_extracts(self):
        """
        Generate a lis of detailed extracts
        """
        for associate in self.associates_data:
            self.generate_detailed_extract(associate_data=associate,
                                           kids_data=self.childs_data[associate['name']])
            # self.current_associate_data = current_associate_data
            # for children_data in self.childs_data:
            #     self.generate_detailed_extract(children_data)


    def generate_detailed_extract(self,associate_data,kids_data):
        """
        Generate a detailed extract with a calendar and
        legend for each child assistance to every activity.
        """
        self.current_associate_data = associate_data
        self.current_child_data = kids_data

        self.mode = 'extract'
        self.generate_header()
        self.generate_footer()
        self.generate_associate_table()
        self.doc.preamble.append(self.first_page)
        
        self.generate_detailed_calendar()
        
        # self.generate_additional_details()
        
        self.generate_file(mode='extract')


    def generate_detailed_calendar(self):
        """
        Generate a calendar table with fields
        according to kids assistance.
        """
        child_attendance_matrices_dict = self.get_child_attendance_rows()
        
        calendar_tabu_spec = f'| X[l] | {(7*"X[c] | ")[:-1]}'
        with self.doc.create(LongTabu(calendar_tabu_spec,
                                      row_height=1.5)) as extract_table:
            extract_table.add_hline()
            extract_table.add_row(self.week_days_row,
                               mapper=bold,
                               color="black")

            for i,week in enumerate(self.matrix_rows_calendar):
                extract_table.add_hline()
                extract_table.add_row(week)
                extract_table.add_hline()
                for monthly_attendance in child_attendance_matrices_dict.values():
                    row = [dumps_list(cell) for cell in monthly_attendance[i]]
                    extract_table.add_row(row)
                extract_table.add_hline()
            extract_table.add_hline()

        self.doc.append(VerticalSpace('8ex'))


    def get_child_attendance_rows(self):
        """
        Generate a dict of attendance

        Args:
            shape (tuple): the shape of the month (num_weeks,7)

        Returns:
            dict: dict with childs as keys and
            values a list of len num days of month
            where each value is a concatenation of
            assistance colored characters
        """
        E = [np.reshape(list(chain(self.initial_month_skip_list,
                                   [list(map(TextColor,
                                             *(self.assigned_colors,daily_attendance)))
                                    for daily_attendance in zip(*activities_dict.values())],
                                   self.final_month_skip_list)),
                        (len(self.matrix_calendar),7)) 
             for activities_dict in child_data.values()]

        attendance_rows_list = [np.concatenate((np.array([child]*len(self.matrix_calendar))[:,None],
                                                monthly_attendance),
                                               axis=1) for child,monthly_attendance in zip(child_data.keys(),E)]

        child_attendance_matrices_dict = dict(zip(child_data.keys(),attendance_rows_list))

        return child_attendance_matrices_dict


    def generate_set_invoices(self):
        for i,associate_data in enumerate(self.associates_data):
            self.generate_invoice(associate_data)
        

    def generate_invoice(self, associate_data):
        """
        Generate invoice from associate data.
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
                title_wrapper.append(TextColor('black',LargeText(bold(f"Fecha: {self.current_associate_data['date']}"))))

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
        Add associate information
        """
        with self.doc.create(Tabular('l|l',
                                     row_height=1.5)) as associate_table:
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
        with self.doc.create(Section('',numbering=False)):
            self.doc.append("FORMA DE PAGO: Domiciliación Bancaria\n")
            self.doc.append("Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")


    def generate_file(self,filename:str='test',mode:str='invoice'):
        """Generate pdf file

        Args:
            filename (str, optional): _description_. Defaults to 'test'.
            mode (str, optional): Defines if it must generate an invoice or a detailed extract. 
            Defaults to 'invoice'.
        """
        ################################### Format page ###################################
        self.doc.change_document_style("firstpage")
        self.doc.add_color(name="lightgray", model="gray", description="0.80")

        ################################## Generate pdf ###################################
        file = f"./{self.current_associate_data['invoice_num']}" if mode == 'invoice' else \
               f"./{self.current_associate_data['invoice_num']}_extract" if mode == 'extract' else \
               filename
        self.doc.generate_pdf(os.path.join(os.path.dirname(__file__),
                                           file),
                              clean_tex=False)


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
        test_quantity = [3, (5,2), (1,0), 0, 0, 0, 10, "6€", "15€", "20€"]
        use = dict(zip(basic_concepts,test_quantity))

        extract = []
        total = 0
        for (concept,quantity) in use.items():
            if isinstance(quantity,tuple):
                subtotal_list = []
                for child_quantity in quantity:
                    if concept.upper() in ["COMEDOR", "ATENCIÓN_TEMPRANA"] and \
                    child_quantity != 0:
                        subtotal_list.append(min(UNIT_PRICE[f'{concept}_MAX'],
                                            child_quantity*UNIT_PRICE[concept]))
                subtotal = sum(subtotal_list)
                extract.append((concept.lower().replace('_',' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))
            elif isinstance(quantity,int):
                if concept.upper() in ["COMEDOR", "ATENCIÓN_TEMPRANA"] and \
                child_quantity != 0:
                    subtotal.append(min(UNIT_PRICE[f'{concept}_MAX'],
                                        child_quantity*UNIT_PRICE[concept]))
                subtotal = quantity*UNIT_PRICE[concept]
                extract.append((concept.lower().replace('_',' '),
                                f"{UNIT_PRICE[concept]:.2f} €",
                                f"{quantity}",
                                f"{subtotal:.2f} €"))

            elif isinstance(quantity,str):
                subtotal = int(quantity[:-1])
                extract.append((concept.lower().replace('_',' '),
                                "",
                                "",
                                f"{subtotal:.2f} €"))

            if subtotal != 0:
                total += subtotal

        extract_tax = [(bold("Base Imponible"),"","",bold(f"{total:.2f} €")),
                    (bold("IVA (exento)"),"","",bold(f"{0:.2f} €")),
                    (bold("Total"),"","",bold(f"{total:.2f} €"))]
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
    id: str=''

@dataclass
class Student:
    """
    A class for students
    
    Args:
        name (str): First name of student
        associate (str): Legal representative, cooperative member
        attendance (dict): keys -> activities, values -> list[str] representing the attendance to activity
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
    data = {#'invoice_num': get_invoice_num(invoice_date),
            #'date': invoice_date.strftime("%d/%m/%y"),
            'name': 'Ejemplo Ejemplez Ejemplez',
            'NIF': '123456789B',
            'adress': 'C/ Dirección. Código Postal, Localidad, Provincia'}

    # generate_invoice(**data)
    instance = PdfGeneration(invoice_num_start=2,associate_data=[data,data])
    from random import choices
    child_data = {
        'Asier': {
            'comedor': choices(['x',''],k=instance.num_monthdays),
            'judo': choices(['x',''],k=instance.num_monthdays)
        },
        'Mike': {
            'comedor': choices(['x',''],k=instance.num_monthdays),
            'judo': choices(['x',''],k=instance.num_monthdays)
        },
    }
    instance.childs_data = child_data
    
    instance.generate_set_invoices()
    instance.generate_detailed_extract(data,child_data)
