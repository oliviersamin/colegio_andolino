'''
Generate invoice
'''
from datetime import date
from json import dumps, loads
import os

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, LongTabu, \
    LineBreak, FootnoteText, Tabular, VerticalSpace, Section, LargeText
# from pylatex import MultiColumn, Tabu, NewLine, Tabularx,
# from pylatex import TextColor, simple_page_number, SmallText, LongTable
from pylatex.utils import bold, NoEscape


########################### Billing concepts ###########################
PRECIO_MAX_COMEDOR = int(os.getenv('PRECIO_MAX_COMEDOR', '20'))
PRECIO_DIA_COMEDOR = int(os.getenv('PRECIO_DIA_COMEDOR', '5'))
PRECIO_MAX_TEMPRANA = int(os.getenv('PRECIO_MAX_TEMPRANA', '20'))
PRECIO_DIA_TEMPRANA = int(os.getenv('PRECIO_DIA_TEMPRANA', '5'))
EXTRAESCOLARES = loads(os.getenv('EXTRAESCOLARES',
                                 '{"JUDO": 25, "CIENCIA": 20, "TEATRO": 20, "ROBOTIX": 20}'))
UNIT_PRICES_DICT = {"CUOTA": 325,
                    "COMEDOR": 5,
                    "COMEDOR_MAX": 25,
                    "ATENCIÓN_TEMPRANA": 5,
                    "ATENCIÓN_TEMPRANA_MAX": 25,
                    "JUDO": 25,
                    "CIENCIA": 20,
                    "TEATRO": 20,
                    "ROBOTIX": 20}
UNIT_PRICE = loads(os.getenv('UNIT_PRICE',
                             dumps(UNIT_PRICES_DICT)))

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


def generate_invoice(**kwargs):
    '''
    Generate invoice
    '''
    ###################################################################################
    ############################ Document Geometry Options ############################
    ###################################################################################

    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "1.6in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)


    ###################################################################################
    ########################### Generating first page style ###########################
    ###################################################################################

    first_page = PageStyle("firstpage")

    # Header image
    with first_page.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                         pos='c')) as logo_wrapper:
            logo_file = os.path.join(os.path.dirname(__file__),
                                     'andolina-logo.png')
            logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
                                filename=logo_file))

    # Add document title
    with first_page.create(Head("R")) as right_header:
        with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                 pos='c', align='l')) as title_wrapper:
            title_wrapper.append(LargeText(bold(f"Número de factura: {kwargs['invoice_num']}")))
            title_wrapper.append(LineBreak())
            title_wrapper.append(LineBreak())
            title_wrapper.append(LargeText(bold(f"Fecha: {kwargs['date']}")))

    # Add footer
    with first_page.create(Foot("L")) as footer:
        footer.append(FootnoteText(f"{LOPD}\n\n\n{COLEGIO_DATOS}"))
        # footer.append(FootnoteText(COLEGIO_DATOS))

    doc.preamble.append(first_page)

    doc.append(VerticalSpace('10ex'))


    ###################################################################################
    ########################### Add associate information #############################
    ###################################################################################

    with doc.create(Tabular('l|l')) as table:
        table.add_row([bold("Nombre:"), kwargs['name']])
        table.add_hline()
        table.add_row([bold("NIF:"), kwargs['NIF']])
        table.add_hline()
        table.add_row([bold("Dirección:"), kwargs['adress']])

    doc.append(VerticalSpace('10ex'))


    ###################################################################################
    ############################## Add invoice details ################################
    ###################################################################################

    with doc.create(LongTabu("X[3l] X[c] X[c] X[c]",
                             row_height=1.5)) as data_table:
        data_table.add_row(["concepto",
                            "precio unitario",
                            "cantidad",
                            "subtotal"],
                           mapper=bold,
                           color="lightgray")
        data_table.add_empty_row()

        extract_final = generate_extract()
        for row in extract_final:
            data_table.add_hline()
            data_table.add_row(row)
            # if (i % 2) == 0:
                # data_table.add_row(row, color="lightgray")
            # else:
                # data_table.add_row(row)

    # with doc.create(LongTabu("X[3r] X[c] X[c] X[c]",
    #                          row_height=1.5)) as data_table:
    #     for row in extract_final[-3:]:
    #         data_table.add_row(row)
    #         data_table.add_hline()

    doc.append(VerticalSpace('10ex'))


    ###################################################################################
    ############################### Add other details #################################
    ###################################################################################

    with doc.create(Section('',numbering=False)):
        doc.append("FORMA DE PAGO: Domiciliación Bancaria\n")
        doc.append("Exención de IVA según el 20.9 de la Ley 37/1992 de 28 de diciembre.")


    ################################### Format page ###################################
    doc.change_document_style("firstpage")
    doc.add_color(name="lightgray", model="gray", description="0.80")

    ################################## Generate pdf ###################################
    doc.generate_pdf(os.path.join(os.path.dirname(__file__),f"./{kwargs['invoice_num']}"), clean_tex=True)


def generate_extract() -> list[tuple]:
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


def get_invoice_num(today: date) -> str:
    '''
    Get current invoice number formated
    Example: FU-2223-001
    '''
    current_year_format = today.year%100
    invoice_num_in_series = 1
    return f'FU-{current_year_format}{current_year_format+1}-{invoice_num_in_series:03}'


if __name__ == '__main__':
    invoice_date = date.today()
    data = {'invoice_num': get_invoice_num(invoice_date),
            'date': invoice_date.strftime("%d/%m/%y"),
            'name': 'Ejemplo Ejemplez Ejemplez',
            'NIF': '123456789B',
            'adress': 'C/ Dirección. Código Postal, Localidad, Provincia'}
    generate_invoice(**data)
