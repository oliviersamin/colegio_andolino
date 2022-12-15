from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from typing import Literal, Optional

@dataclass
class Adress:
    street_and_number: str
    postal_code: int
    city: str
    
    def __repr__(self) -> str:
        return f'{self.street_and_number}, {self.postal_code}, {self.city}'

@dataclass
class Person:
    name: str
    adress: Adress
    NIF: str


@dataclass
class Associate(Person):
    """
    A class for associates
    """
    associate_type : Literal['presocio', 'socio', 'colaborador']
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

# Enrollment / impreso de matrícula
@dataclass
class ChildInfo(Person):
    """Enrollment child data
    """
    birthdate: str
    birthplace: str
    num_siblings: str
    position_siblings: str
    nationality: str

class PreviousSchooling:
    """_summary_
    """
    previously_schooled: Literal['sí','no']
    previous_school : str = ''
    educational_support: Literal['sí','no', ''] = ''
    report_compromise: Literal['sí','no', ''] = ''


@dataclass
class Signature:
    city: str
    signature: str
    date: str = field(default_factory=lambda: date.today().strftime('%d-%m-%Y'))

@dataclass
class Parent(Person):
    """Associate, parent, legal tutor or legal representant of Andolina
    """
    relation_with_child: Literal['madre','padre','tutora legar','tutor legal','otro']
    # parent : Person
    education: str  # =''
    occupation: str # =''
    phone: str  # =''
    email: str      # =''
    signature: Signature

@dataclass
class Enrollment_contact:
    allow_contact: Literal['sí', 'no']

@dataclass
class Enrollment:
    academyc_year: str
    child_info: ChildInfo
    previous_schooling: PreviousSchooling
    parent1: Parent
    parent2: Parent
    enrollment_contact: Enrollment_contact

# LOPD form / Cláusula LOPD - Socios Cooperativistas
@dataclass
class LOPDForm:
    signature: Signature
    date: str = field(default_factory=lambda: date.today().strftime('%d-%m-%Y'))

# Image posting authorization / Autorización para la publicación de imágenes
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
    children: list[Person]
    self_authorization: Literal['sí', 'no']
    children_authorization: Literal['sí', 'no']
    auth_Andolina: str = '' # Parent = Parent(*['']*9)
    date: str = field(default_factory=lambda: date.today().strftime('%d-%m-%Y'))

# outing authorization / Autorización para salidas escolares
@dataclass
class OutingAuthorization:
    """School outing authorization.
    
    arg1 = "DOY MI AUTORIZACIÓN a cualquier excursión organizada o salida espontánea "
    "que surja de 9:30 a 14:00 de la mañana, "
    "a lo largo del presente curso y los sucesivos, salvo revocación expresa."
    arg2 = "Marcando esta casilla indico que no estoy de acuerdo "
    "con que se utilicen vehículos particulares "
    "para el transporte de mi hijo/a."
    """
    parent: Parent
    child: Person
    personal_vehicle_authorization: Literal['sí', 'no']

# Health info / Formulario de Salud, Información de Salud - Alergias
@dataclass
class Diseases:
    """Known conditions and hospitalization past"""
    conditions: str
    hospitalized: str
    conditions_comments: str = ''

@dataclass
class Allergies:
    """Known allergies"""
    allergies: str
    manifestations: str
    triggers: str
    treatment: str
    allergies_comments: str = ''

@dataclass
class Intolerances:
    """Known intollerances"""
    intolerances: str
    intolerances_comments: str

@dataclass
class Vaccines:
    tetanos: str
    vaccines_comments: str

@dataclass
class HealthContacts:
    professional_contact_name: str
    professional_contact_phone: str
    family_contact: Parent
    
    def __repr__(self) -> str:
        return (f'Contacto profesional: {self.professional_contact_name} {self.professional_contact_phone}\n'
                f'Contacto personal: {self.family_contact.fullname} {self.family_contact.phone} ({self.family_contact.relation_with_child})')

@dataclass
class HealthInfo:
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
    child: ChildInfo
    parent: Parent
    diseases: Diseases
    allergies: Allergies
    intolerances: Intolerances
    vaccines: Vaccines
    health_contacts: HealthContacts
    important_info_comments: str = ''
    date: str = field(default_factory=lambda: date.today().strftime('%d-%m-%Y'))


# Possible validations
class Binario(Enum):
    SI = auto()
    NO = auto()


class AssociateType(Enum):
    """Different types of associates."""
    COLABORADOR = auto()
    SOCIO = auto()


class LegalRelation(Enum):
    MADRE = auto()
    PADRE = auto()
    TUTORA_LEGAL = auto()
    TUTOR_LEGAL = auto()