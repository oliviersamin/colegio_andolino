import os
from json import loads as jloads
from json import dumps as jdumps


# Forms related constants
PUBLIC_CHOICE_ACTIVITY_FORM = [('children', 'children'), ('parents', 'parents')]
PERMISSION_ACTIVITY_CHOICES = [('Creator only', 'Creator only'), ('Group only', 'Group only'), ('Several groups', 'Several groups'), ('All', 'All')]

### Bill generation coming from Miguel script
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

# Information Strings
COLEGIO_NOMBRE = os.getenv("COLEGIO_NOMBRE",
                           "Colegio Andolina Sociedad Cooperativa Asturiana")
COLEGIO_CIF = os.getenv("COLEGIO_NOMBRE",
                        "F33986522")
COLEGIO_DIRECCION = os.getenv("COLEGIO_DIRECCION",
                              ("Camino del Barreo, 203"
                               "Cefontes (Cabueñes) 33394 Gijón Asturias."))
COLEGIO_DATOS = os.getenv("COLEGIO_DATOS",
                          f'{COLEGIO_NOMBRE} - CIF:'
                          f'{COLEGIO_CIF} - {COLEGIO_DIRECCION}')
PAYMENT_METHOD = os.getenv("PAYMENT_METHOD",
                           "FORMA DE PAGO: Domiciliación Bancaria.")
EXEMPTION = os.getenv("EXEMPTION",
                      ("Exención de IVA según el 20.9 de la Ley 37/1992"
                       "de 28 de diciembre."))
LOPD = os.getenv("LOPD",
                 ("A los efectos previstos en la Ley Orgánica 15/1999, "
                  "de 13 de diciembre, "
                  "sobre Protección de Datos de Carácter Personal, "
                  "se le informa que los datos personales proporcionados "
                  "se incorporarán a los ficheros de "
                  "Colegio Andolina Sociedad Cooperativa Asturiana, "
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
