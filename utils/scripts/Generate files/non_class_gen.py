
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
