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


"""
ENVIRONMENT VARIABLES
"""
# Billing concepts
PRECIO_MAX_COMEDOR = int(os.getenv('PRECIO_MAX_COMEDOR', '20'))
PRECIO_DIA_COMEDOR = int(os.getenv('PRECIO_DIA_COMEDOR', '5'))
PRECIO_MAX_TEMPRANA = int(os.getenv('PRECIO_MAX_TEMPRANA', '20'))
PRECIO_DIA_TEMPRANA = int(os.getenv('PRECIO_DIA_TEMPRANA', '5'))
EXTRAESCOLARES = jloads(os.getenv('EXTRAESCOLARES',
                                  ('{"JUDO": 25,'
                                   '"CIENCIA": 20,'
                                   '"TEATRO": 20,'
                                   '"ROBOTIX": 20}')))
ACTIVIDADES_ESCOLARES = ['COLEGIO',
                         'ATENCIÓN TEMPRANA',
                         'COMEDOR']
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
CASES = os.getenv('CASES',
                  ['invoice',
                   'extract',
                   'enrollment',
                   'direct debit',
                   'LOPD',
                   'image posting',
                   'school outings',
                   'health report',])
"""
case 'invoice':
case 'extract':
case 'enrollment':
case 'direct debit':
case 'LOPD':
case 'image posting':
case 'school outings':
case 'health report':
"""
# Information Strings
COLEGIO_NOMBRE = os.getenv("COLEGIO_NOMBRE",
                           "Colegio Andolina Sociedad Cooperativa Asturiana")
COLEGIO_CIF = os.getenv("COLEGIO_NOMBRE",
                        "F33986522")
COLEGIO_DIRECCION = os.getenv("COLEGIO_DIRECCION",
                              ("Camino del Barreo, 203"
                               "Cefontes (Cabueñes) 33394 Gijón Asturias."))
COLEGIO_TELEFONO = os.getenv("COLEGIO_TELEFONO",
                             "683 17 81 94")
COLEGIO_DPO = os.getenv("COLEGIO_DPO",
                        "lopd@colegioandolina.org")
COLEGIO_DATOS = os.getenv("COLEGIO_DATOS",
                          f'{COLEGIO_NOMBRE} - CIF: '
                          f'{COLEGIO_CIF} - {COLEGIO_DIRECCION}; '
                          f'contacto DPO: {COLEGIO_DPO}.')
CLAUSULA_PROT_DATOS = ("Te informamos de la incorporación de tus datos "
                       "a los sistemas de información del responsable de tratamiento: "
                       f"{COLEGIO_DATOS} "
                       "Las finalidades para las que tratamos los datos "
                       "que nos facilitas son: "
                       "Estudio y gestión de tu solicitud de admisión como socio/a, "
                       "en calidad de usuario/colaborador, "
                       "y creación de estadísticas de la cooperativa para uso interno. "
                       "En caso de admisión: "
                       "para la creación de la cuenta de usuario en los sistemas del Responsable; "
                       "mantenimiento, desarrollo y/o control del cumplimiento "
                       "de la relación de cooperación, "
                       "una vez sea admitida la solicitud; "
                       "gestión del proceso de escolarización del/la menor o menores; "
                       "seguimiento y comunicación del progreso del/la menor o menores, "
                       "así como de actividades, comportamientos y/o "
                       "hechos derivados de la actividad escolar; "
                       "atención de tus consultas y solicitudes; "
                       "control de calidad; gestión administrativa, "
                       "económica y contable asociada a la prestación de nuestros servicios "
                       "y/o a la relación con el cedente de datos, "
                       "así como en caso de que haya consentido, "
                       "para las finalidades descritas en los consentimientos "
                       "adicionales que sean solicitados. "
                       "En relación con tus derechos, "
                       "te informamos de que podrás acceder, "
                       "rectificar y suprimir los datos, así como limitar, "
                       "retirar u oponerse al tratamiento conforme a los procedimientos establecidos "
                       "en nuestra política de privacidad. "
                       "Si consideras que el ejercicio de tus derechos no ha sido plenamente satisfactorio, "
                       "podrás presentar una reclamación ante la autoridad nacional de control "
                       "dirigiéndote a estos efectos a la Agencia Española de Protección de Datos, "
                       "C/ Jorge Juan, 6 - 28001 Madrid. "
                       "Los datos personales que tratamos proceden del propio interesado "
                       "o su representante legal, así como de familiares y/o allegados. "
                       "La estructura de datos que tratamos puede contener datos sensibles, "
                       "relacionados con necesidades específicas del/la menor o menores "
                       "señalados en la solicitud, siendo, en este caso, "
                       "necesario facilitar documentación que acredite o justifique las mismas. "
                       "Puedes consultar la información adicional y detallada sobre "
                       "Protección de Datos en la Política de Privacidad "
                       f"a solicitud al email {COLEGIO_DPO}.")
CLAUSULA_PROT_DATOS_PERSONAL = os.getenv('CLAUSULA_PROT_DATOS_PERSONAL',
                                         "El contacto y envío de comunicaciones relacionadas con la actividad "
                                         "del Responsable, así como invitarte a eventos e informarte de noticias "
                                         "que pudieran resultar de tu interés, a través de los medios de comunicación facilitados. \n"
                                         "Con la aceptación y/o validación del proceso, "
                                         "declaras ser mayor de 14 años y disponer de capacidad jurídica* "
                                         "y consientes expresamente el tratamiento de datos "
                                         "conforme a lo establecido en la cláusula e información adicional "
                                         "sobre protección de datos. "
                                         "Asimismo, declaras disponer del consentimiento de terceros "
                                         "de los que nos facilites datos personales para dicho tratamiento. "
                                         "Si has marcado la casilla correspondiente de consentimiento, "
                                         "la base legal para dichos fines es tu consentimiento, "
                                         "que puedes retirar en cualquier momento. \n"
                                         "(*)Declara responsablemente disponer de la patria potestad "
                                         "o tutela del menor o de la representación legal jurídica correspondiente, "
                                         "cuya justificación podrá ser requerida por parte del "
                                         "Responsable de Tratamiento a fin de legitimar el consentimiento aceptado."
                                         )
CONS_CLAUS_PROT_DATOS_PERSONAL = os.getenv('CONS_CLAUS_PROT_DATOS_PERSONAL',
                                           "D/Dª …………………………………………………………………………………………………………, "
                                           "con NIF o pasaporte Nº ………………………… como titular o representante legal del mismo, "
                                           "consiente de forma inequívoca la presente cláusula "
                                           "y política de privacidad de protección de datos de carácter personal:"
                                           )
LOPD_COOP = os.getenv('LOPD_COOP',
                      "En cumplimiento de lo dispuesto en la Ley Orgánica 15/1999, de 13 de diciembre, "
                      "de Protección de Datos de Carácter Personal, "
                      f"{COLEGIO_NOMBRE} "
                      "informa al socio que los datos personales recabados en el momento en el momento inicial "
                      "(solicitud de entrada a la sociedad) así como los obtenidos o generados en el transcurso de la relación "
                      "(DNI, Libro de Familia, domiciliación bancaria, Impreso de Matrícula, imágenes y audios, datos del/los hijo/s, etc.) "
                      "serán incorporados/actualizados a un fichero titularidad de la sociedad "
                      "cuya finalidad es la gestión global de la misma, "
                      "y le reconoce la posibilidad de ejercitar gratuitamente los derechos de acceso, "
                      "rectificación, cancelación y oposición sobre tales datos mediante comunicación "
                      f"escrita dirigida a {COLEGIO_DATOS}. \n"
                      f"Igualmente, {COLEGIO_NOMBRE} le informa que cederá sus datos "
                      "a todo organismo público al que esté obligado por la ley, "
                      "que los utilizarán en ejercicio de las funciones o competencias que tengan establecidas. \n"
                      "Además, sus datos podrán ser comunicados a las entidades de crédito "
                      "a través de las cuales se realiza el cobro de cuotas y otros pagos establecidos, "
                      "que los emplearán para efectuar la transferencia. \n"
                      "Si, entre la información facilitada por el socio, "
                      "figuran datos de terceros (cónyuges o hijos principalmente), "
                      "éste asume el compromiso de informarles de los extremos señalados en los párrafos precedentes. \n"
                      "Mediante la firma de esta cláusula el socio autoriza expresamente a "
                      f"{COLEGIO_NOMBRE} para tratar sus datos en los términos descritos")
CONFIDENCIALIDAD = os.getenv('CONFIDENCIALIDAD',
                             "El socio se compromete a guardar absoluto secreto y confidencialidad "
                             f"respecto de cualquier información, tanto de {COLEGIO_NOMBRE} "
                             "como de otras empresas/personas físicas con la que éste mantiene relaciones y acuerdos, "
                             "a la que pudiera tener acceso como consecuencia del desempeño de su cargo de socio y, "
                             "en especial, de aquélla que contenga datos de carácter personal, "
                             "obligación que subsistirá incluso después de finalizar sus relaciones con "
                             f"{COLEGIO_NOMBRE}. \n"
                             "El incumplimiento de la obligación de confidencialidad podrá dar lugar a "
                             "las sanciones disciplinarias que correspondan en atención a la gravedad de los hechos, "
                             "sin perjuicio de la exigencia de indemnizaciones por daños y perjuicios, "
                             "de acuerdo con lo dispuesto en la mencionada Ley, "
                             "en el artículo 1101 y concordantes del Código Civil, "
                             "y en la Ley de Propiedad Intelectual.")
POL_PROT_DATOS = os.getenv('POL_PROT_DATOS',
                           "Con la firma de la presente cláusula, el socio se declara informado acerca de "
                           "la existencia de la Política de Protección de Datos de la empresa, "
                           "que se encuentra a su disposición en las instalaciones de la entidad, "
                           "y se compromete a cumplir los deberes u obligaciones que en ella se establecen "
                           "en materia de protección de datos de carácter personal.")
PUB_IMAG = os.getenv('PUB_IMAG',
                     "Para dar cumplimiento a lo establecido en el Reglamento (UE) 2016/679 "
                     "del Parlamento Europeo y del Consejo, de 27 de "
                     "abril de 2016, relativo a la protección de las personas físicas "
                     "en lo que respecta al tratamiento de datos personales y a la libre "
                     "circulación de estos datos; "
                     "a las Recomendaciones e Instrucciones emitidas por la Agencia Española de Protección de Datos (A.E.P.D.), "
                     "así como a lo dispuesto en el artículo 18 de la Constitución y en la "
                     "Ley 1/1982, de 5 de mayo, sobre el derecho al honor, a la intimidad "
                     "personal y familiar y a la propia imagen y en el Reglamento referenciado, "
                     "por medio del presente documento te informamos de lo siguiente: \n"
                     "Tus datos (imagen y/o voz obtenidos mediante la grabación de videos y/o "
                     "fotografías realizados durante la celebración de "
                     "eventos, jornadas, y otras actividades que el Responsable "
                     "pudiera llevar a cabo con motivo de la gestión del curso escolar), "
                     f"serán incorporados a los sistemas de Tratamiento de {COLEGIO_NOMBRE} "
                     "(Responsable del Tratamiento), con la finalidad de "
                     "difundirlos en redes sociales corporativa "
                     "(con carácter informativo y no limitativo, Facebook®, YouTube®, Twitter®, Instagram®) "
                     "así como en la página web o como elemento de publicidad, "
                     "marketing o difusión en otros medios (públicos y/o privados), "
                     "además de para uso interno de la cooperativa "
                     "(reuniones de familias, intranet, etc.), "
                     "sin restricción territorial o temporal. \n"
                     "La legitimidad del tratamiento es el consentimiento expreso del interesado "
                     "que se solicita a través de la presente cláusula. \n"
                     "Te informamos de que los datos se conservaran mientras no se solicite su supresión, "
                     "con excepción de la posible conservación para la defensa de reclamaciones "
                     "del responsable de tratamiento o con miras a la protección de los derechos de otra "
                     "persona física o jurídica y/o por razones de obligación legal. \n"
                     "Se realizaran comunicaciones legítimas a "
                     "entidades relacionadas con el responsable "
                     "de tratamiento para las finalidades descritas, "
                     "o por consentimiento inequívoco. "
                     "No están previstas transferencias internacionales de sus datos. \n"
                     "Te informamos de que puede acceder, rectificar y suprimir los datos, "
                     "así como limitar, retirar u oponerte al tratamiento "
                     "conforme a los procedimientos establecidos en nuestra política de privacidad. "
                     "Los datos que tratamos proceden del propio interesado o su representante legal. \n"
                     "La estructura de datos no contiene datos relativos a "
                     "condenas e infracciones penales, ni datos especialmente protegidos. \n"
                     "En todo caso, tienes derecho a presentar una reclamación ante "
                     "la autoridad de protección de datos competente (www.aepd.es). \n"
                     "Puede consultar la información adicional y detallada en la "
                     f"Política de Privacidad disponible mediante solicitud al correo electrónico {COLEGIO_DPO}.")
LOPD = os.getenv("LOPD",
                 ("A los efectos previstos en la Ley Orgánica 15/1999, "
                  "de 13 de diciembre, "
                  "sobre Protección de Datos de Carácter Personal, "
                  "se le informa que los datos personales proporcionados "
                  "se incorporarán a los ficheros de "
                  f"{COLEGIO_NOMBRE}, "
                  f"con dirección en {COLEGIO_DIRECCION} "
                  "La finalidad del tratamiento de los datos será "
                  "la de gestionar los servicios suministrados. "
                  "Usted tiene derecho al acceso, rectificación, "
                  "cancelación y "
                  "oposición en los términos previstos en la Ley, "
                  "que podrá ejercitar mediante escrito "
                  "dirigido al responsable de los mismos "
                  "en la dirección anteriormente indicada "
                  "o a la dirección de correo electrónico "
                  "lopd@colegioandolina.org."))
VERSION_LOPD = os.getenv('VERSION_LOPD',
                         '25/2/2016 y Versión 1.1')
INFO_DATOS_MEDICOS = os.getenv('INFO_DATOS_MEDICOS',
                               "Los datos que se piden en el presente cuestionario "
                               "permitirán a los equipos pedagógicos del colegio "
                               "conocer mejor a nuestros alumnos/as "
                               "y los consideramos fundamentales para su salud "
                               "y su correcto desarrollo educativo. "
                               "Esta información, como el resto aportada en la solicitud de matrícula, "
                               "tienen la consideración de confidenciales.")

COLORS = ["black",
          "blue",
          "brown",  # "cyan", "darkgray", "gray",
          "green",  # "lightgray", "lime", "magenta", "olive",
          "orange",  # "pink",
          "purple",
          "red",
          "teal",
          "violet",  # "white",
          "yellow"]
activities_colors_dict = dict(zip(ACTIVIDADES, COLORS))

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
                assert all(isinstance(student,Students) for student in data), f'{TypeError} {data} is not of Students type'
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
            for activity, color in activities_colors_dict.items():
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
    NIF: str = field(default_factory=lambda: '')

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
    education: str  # =field(default_factory=lambda: '')
    occupation: str # =field(default_factory=lambda: '')
    telephone: str  # =field(default_factory=lambda: '')
    email: str      # =field(default_factory=lambda: '')

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
    important_info: str = field(default_factory=lambda: '')
    date: str = field(default_factory=lambda: date.today().strftime('%Y-%m-%d'))

    outing_permission: str = field(default_factory=lambda: '')
    private_vehicle: str = field(default_factory=lambda: '')

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
    important_info_comments: str = field(default_factory=lambda: '')
    date: str = field(default_factory=lambda: date.today().strftime('%Y-%m-%d'))
    
    allergies = Literal['sí','no']
    manifestations: str = field(default_factory=lambda: '')
    trigger: str = field(default_factory=lambda: '')
    treatment = Literal['sí','no']
    allergies_comments: str = field(default_factory=lambda: '')
    
    intolerances = Literal['sí','no']
    intolerances_comments: str = field(default_factory=lambda: '')
    
    vaccines = Literal['sí','no']
    vaccines_comments: str = field(default_factory=lambda: '')
    
    pro_emergency_contact: list = field(default_factory=lambda: ['',''])
    fam_emergency_contact: list = field(default_factory=lambda: ['',''])


    