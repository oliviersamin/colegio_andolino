from json import dumps, loads
import os

PRECIO_MAX_COMEDOR = int(os.getenv("PRECIO_MAX_COMEDOR", "20"))
PRECIO_DIA_COMEDOR = int(os.getenv("PRECIO_DIA_COMEDOR", "5"))
PRECIO_MAX_TEMPRANA = int(os.getenv("PRECIO_MAX_TEMPRANA", "20"))
PRECIO_DIA_TEMPRANA = int(os.getenv("PRECIO_DIA_TEMPRANA", "5"))
EXTRAESCOLARES = loads(
    os.getenv(
        "EXTRAESCOLARES",
        ('{"JUDO": 25,' '"CIENCIA": 20,' '"TEATRO": 20,' '"ROBOTIX": 20}'),
    )
)
ACTIVIDADES_ESCOLARES = ["COLEGIO", "ATENCIÓN TEMPRANA", "COMEDOR"]
ACTIVIDADES = ACTIVIDADES_ESCOLARES
ACTIVIDADES.extend(EXTRAESCOLARES.keys())
UNIT_PRICES_DICT = {
    "CUOTA": 325,
    "COMEDOR": 5,
    "COMEDOR_MAX": 25,
    "ATENCIÓN_TEMPRANA": 5,
    "ATENCIÓN_TEMPRANA_MAX": 25,
    "JUDO": 25,
    "CIENCIA": 20,
    "TEATRO": 20,
    "ROBOTIX": 20,
}
UNIT_PRICE = loads(os.getenv("UNIT_PRICE", dumps(UNIT_PRICES_DICT)))
CASES = os.getenv(
    "CASES",
    [
        "invoice",
        "extract",
        "enrollment",
        "direct debit",
        "LOPD",
        "image posting",
        "school outings",
        "health report",
    ],
)
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
COLEGIO_NOMBRE = os.getenv(
    "COLEGIO_NOMBRE", "Colegio Andolina Sociedad Cooperativa Asturiana"
)
COLEGIO_CIF = os.getenv("COLEGIO_NOMBRE", "F33986522")
COLEGIO_DIRECCION = os.getenv(
    "COLEGIO_DIRECCION",
    ("Camino del Barreo, 203" "Cefontes (Cabueñes) 33394 Gijón Asturias."),
)
COLEGIO_TELEFONO = os.getenv("COLEGIO_TELEFONO", "683 17 81 94")
COLEGIO_DPO = os.getenv("COLEGIO_DPO", "lopd@colegioandolina.org")
COLEGIO_DATOS = os.getenv(
    "COLEGIO_DATOS",
    f"{COLEGIO_NOMBRE} - CIF: "
    f"{COLEGIO_CIF} - {COLEGIO_DIRECCION}; "
    f"contacto DPO: {COLEGIO_DPO}.",
)
CLAUSULA_PROT_DATOS = (
    "Te informamos de la incorporación de tus datos "
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
    f"a solicitud al email {COLEGIO_DPO}."
)
CLAUSULA_PROT_DATOS_PERSONAL = os.getenv(
    "CLAUSULA_PROT_DATOS_PERSONAL",
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
    "Responsable de Tratamiento a fin de legitimar el consentimiento aceptado.",
)
CONS_CLAUS_PROT_DATOS_PERSONAL = os.getenv(
    "CONS_CLAUS_PROT_DATOS_PERSONAL",
    "D/Dª …………………………………………………………………………………………………………, "
    "con NIF o pasaporte Nº ………………………… como titular o representante legal del mismo, "
    "consiente de forma inequívoca la presente cláusula "
    "y política de privacidad de protección de datos de carácter personal:",
)
LOPD_COOP = os.getenv(
    "LOPD_COOP",
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
    f"{COLEGIO_NOMBRE} para tratar sus datos en los términos descritos",
)
CONFIDENCIALIDAD = os.getenv(
    "CONFIDENCIALIDAD",
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
    "y en la Ley de Propiedad Intelectual.",
)
POL_PROT_DATOS = os.getenv(
    "POL_PROT_DATOS",
    "Con la firma de la presente cláusula, el socio se declara informado acerca de "
    "la existencia de la Política de Protección de Datos de la empresa, "
    "que se encuentra a su disposición en las instalaciones de la entidad, "
    "y se compromete a cumplir los deberes u obligaciones que en ella se establecen "
    "en materia de protección de datos de carácter personal.",
)
PUB_IMAG = os.getenv(
    "PUB_IMAG",
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
    f"Política de Privacidad disponible mediante solicitud al correo electrónico {COLEGIO_DPO}.",
)
LOPD = os.getenv(
    "LOPD",
    (
        "A los efectos previstos en la Ley Orgánica 15/1999, "
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
        "lopd@colegioandolina.org."
    ),
)
VERSION_LOPD = os.getenv("VERSION_LOPD", "25/2/2016 y Versión 1.1")
INFO_DATOS_MEDICOS = os.getenv(
    "INFO_DATOS_MEDICOS",
    "Los datos que se piden en el presente cuestionario "
    "permitirán a los equipos pedagógicos del colegio "
    "conocer mejor a nuestros alumnos/as "
    "y los consideramos fundamentales para su salud "
    "y su correcto desarrollo educativo. "
    "Esta información, como el resto aportada en la solicitud de matrícula, "
    "tienen la consideración de confidenciales.",
)

COLORS = [
    "black",
    "blue",
    "brown",  # "cyan", "darkgray", "gray",
    "green",  # "lightgray", "lime", "magenta", "olive",
    "orange",  # "pink",
    "purple",
    "red",
    "teal",
    "violet",  # "white",
    "yellow",
]
ACTIVITIES_COLORS_DICT = dict(zip(ACTIVIDADES, COLORS))
