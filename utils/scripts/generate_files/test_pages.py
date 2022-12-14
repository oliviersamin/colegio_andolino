from pylatex import Document, Head, MiniPage, NoEscape, StandAloneGraphic, VerticalSpace, LargeText, LineBreak, TextColor, PageStyle, NewPage
from pylatex.utils import bold
from datetime import date
import os
GEOMETRY_OPTIONS = {
    "head": "40pt",
    "margin": "0.5in",
    "bottom": "1.6in",
    "includeheadfoot": True
    }

geometry_options = GEOMETRY_OPTIONS
doc = Document(geometry_options=geometry_options)

current_associate_data = {
    'name': 'Mike',
    'invoice_num' : 1,
    'date': date.today()
}

first_page = PageStyle("firstpage")
doc.change_page_style("firstpage")

doc.preamble.append(first_page)
with first_page.create(Head("L")) as header_left:
            with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                             pos='c')) as logo_wrapper:
                logo_file = os.path.join(os.path.dirname(__file__),
                                         'andolina-logo.png')
                logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
                                                      filename=logo_file))

# Left Header: Document Title
with first_page.create(Head("R")) as right_header:
    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                        pos='c',
                                        align='l')) as title_wrapper:
        title_wrapper.append(LargeText(bold(f"Número de factura: {current_associate_data['invoice_num']}")))
        title_wrapper.append(LineBreak())
        title_wrapper.append(LineBreak())
        title_wrapper.append(TextColor('black',
                                        LargeText(bold(f"Fecha: {current_associate_data['date']}"))))


doc.append(VerticalSpace('8ex'))
doc.append('this is some text')
doc.append(NewPage())

second_page = PageStyle("secondpage")
print(second_page.name)
doc.change_page_style("secondpage")

doc.preamble.append(second_page)
with second_page.create(Head("L")) as header_left:
            with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                             pos='c')) as logo_wrapper:
                logo_file = os.path.join(os.path.dirname(__file__),
                                         'andolina-logo.png')
                logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
                                                      filename=logo_file))

# Left Header: Document Title
with second_page.create(Head("R")) as right_header:
    with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
                                        pos='c',
                                        align='l')) as title_wrapper:
        title_wrapper.append(LargeText(bold(f"Número de factura2: {current_associate_data['invoice_num']}")))
        title_wrapper.append(LineBreak())
        title_wrapper.append(LineBreak())
        title_wrapper.append(TextColor('black',
                                        LargeText(bold(f"Fecha: {current_associate_data['date']}"))))


doc.append(VerticalSpace('8ex'))
doc.append('this is some other text')


doc.append(NewPage())
doc.append('new text')

# second_page = PageStyle("secondpage")
# doc.change_page_style(second_page)
# with second_page.create(Head("L")) as header_left:
#             with header_left.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
#                                              pos='c')) as logo_wrapper:
#                 logo_file = os.path.join(os.path.dirname(__file__),
#                                          'andolina-logo.png')
#                 logo_wrapper.append(StandAloneGraphic(image_options="width=200px",
#                                                       filename=logo_file))

# # Left Header: Document Title
# with second_page.create(Head("R")) as right_header:
#     with right_header.create(MiniPage(width=NoEscape(r"0.5\textwidth"),
#                                         pos='c',
#                                         align='l')) as title_wrapper:
#         title_wrapper.append(LargeText(bold(f"Número de factura2: {current_associate_data['invoice_num']}")))
#         title_wrapper.append(LineBreak())
#         title_wrapper.append(LineBreak())
#         title_wrapper.append(TextColor('black',
#                                         LargeText(bold(f"Fecha2: {current_associate_data['date']}"))))


# doc.append(VerticalSpace('8ex'))
# doc.append('this is some diff text')
# doc.preamble.append(second_page)

# doc.add_color(name="lightgray", model="gray", description="0.80")

# Generate pdf
file = f"./{current_associate_data['invoice_num']}"
doc.generate_pdf(os.path.join(os.path.dirname(__file__),
    file),
clean_tex=True)