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
    previously_schooled: bool  # Literal['sí','no']
    previous_school : str = ''
    educational_support: bool  # Literal['sí','no', ''] = ''
    report_compromise: bool  # Literal['sí','no', ''] = ''


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
    allow_contact: bool  # Literal['sí', 'no']

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
    self_authorization: bool  # Literal['sí','no'] 
    children_authorization: bool  # Literal['sí','no'] 
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
    personal_vehicle_authorization: bool  # Literal['sí','no'] 

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



###################################### MODELS ###########################################
class ImpresoDeMatricula:
    academyc_year: str
    
    # child_info: ChildInfo
    child_name: str 
    child_adress: str
    child_NIF: str = ''
    child_birthdate: str
    child_birthplace: str
    child_num_siblings: str
    child_position_siblings: str
    child_nationality: str
    
    # previous_schooling: PreviousSchooling
    previously_schooled: bool  # Literal['sí','no']
    previous_school : str = ''
    educational_support: bool  # Literal['sí','no', ''] = ''
    report_compromise: bool  # Literal['sí','no', ''] = ''

    # parent1: Parent
    parent1_name: str
    parent1_adress: str
    parent1_NIF: str
    parent1_relation_with_child: Literal['madre','padre','tutora legar','tutor legal','otro']
    parent1_education: str
    parent1_occupation: str
    parent1_phone: str
    parent1_email: str
    # parent1_signature: Signature
    parent1_city: str
    parent1_signature: str
    parent1_date: str = date.today().strftime('%d-%m-%Y')

    # parent2: Parent
    parent2_name: str
    parent2_adress: str
    parent2_NIF: str
    parent2_relation_with_child: Literal['madre','padre','tutora legar','tutor legal','otro']
    parent2_education: str
    parent2_occupation: str
    parent2_phone: str
    parent2_email: str
    # parent2_signature: Signature
    parent2_city: str
    parent2_signature: str
    parent2_date: str = date.today().strftime('%d-%m-%Y')
    
    enrollment_contact: bool


class DomiciliacionBancaria:
    name: str
    adress: str
    postal_code: str
    city: str
    country: str
    account_number: str # either Swift BIC of 8 or 11 char or IBAN of 24 char starting with ES
    recurrent_payment: bool
    # signature: Signature
    city: str
    signature: str
    date: str = date.today().strftime('%d-%m-%Y')

class LOPD:
    # signature: Signature
    city: str
    signature: str
    date: str = date.today().strftime('%d-%m-%Y')

class Child:
    name: str
    adress: str
    NIF: str = ''

class ImageAuthorization:
    # parent1: Parent
    parent1_name: str
    parent1_adress: str
    parent1_NIF: str
    # parent1_signature: Signature
    parent1_city: str
    parent1_signature: str
    parent1_date: str = date.today().strftime('%d-%m-%Y')

    # parent2: Parent
    parent2_name: str
    parent2_adress: str
    parent2_NIF: str
    # parent2_signature: Signature
    parent2_city: str
    parent2_signature: str
    parent2_date: str = date.today().strftime('%d-%m-%Y')

    children = list[Child]
    adult_authorization: bool
    children_authorization: bool 
    auth_Andolina: str = ''
    date: str = date.today().strftime('%d-%m-%Y')
    

class OutingAuthorization:
    """School outing authorization.
    
    arg1 = "DOY MI AUTORIZACIÓN a cualquier excursión organizada o salida espontánea "
    "que surja de 9:30 a 14:00 de la mañana, "
    "a lo largo del presente curso y los sucesivos, salvo revocación expresa."
    arg2 = "Marcando esta casilla indico que no estoy de acuerdo "
    "con que se utilicen vehículos particulares "
    "para el transporte de mi hijo/a."
    """
    parent_name: str
    parent_NIF: str
    relation: Literal['padre','madre','tutor','tutora']
    child_name: str
    personal_vehicle_authorization: bool
    parent_city: str
    parent_signature: str
    parent_date: str = date.today().strftime('%d-%m-%Y')

class HealthReport:
    child_name: str
    child_birth: str

    conditions: bool
    ongoing_conditions: str = ''
    hospitalized: bool
    why_hospitalized: str = ''
    
    allergies: bool
    allergies_manifestations: str = ''
    allergies_triggers: str = ''
    allergies_treatment: str = ''
    allergies_comments: str = ''
    
    intolerances: bool
    intolerances_comments: str = ''
    
    tetanos_vaccine: bool
    vaccines_comments: str = ''

    professional_contact_name: str  = ''
    professional_contact_number: str = ''
    family_contact_name: str
    family_contact_number: str
    family_contact2_name: str = ''
    family_contact2_number: str = ''
        
    important_info_comments: str = ''
    
    parent_name: str
    parent_NIF: str
    parent_city: str
    parent_signature: str
    parent_date: str = date.today().strftime('%d-%m-%Y')
    
################################# PACK DE BIENVENIDA MODEL #################################

class PackBienvenida:
    academyc_year: str
    
    # child_info: ChildInfo
    child_name: str 
    child_adress: str
    child_NIF: str = ''
    child_birthdate: str
    child_birthplace: str
    child_num_siblings: str
    child_position_siblings: str
    child_nationality: str
    
    # previous_schooling: PreviousSchooling
    previously_schooled: bool  # Literal['sí','no']
    previous_school : str = ''
    educational_support: bool  # Literal['sí','no', ''] = ''
    report_compromise: bool  # Literal['sí','no', ''] = ''

    # parent1: Parent
    parent1_name: str
    parent1_adress: str
    parent1_NIF: str
    parent1_relation_with_child: Literal['madre','padre','tutora legar','tutor legal','otro']
    parent1_education: str
    parent1_occupation: str
    parent1_phone: str
    parent1_email: str
    # parent1_signature: Signature
    parent1_city: str
    parent1_signature: str
    parent1_date: str = date.today().strftime('%d-%m-%Y')

    # parent2: Parent
    parent2_name: str
    parent2_adress: str
    parent2_NIF: str
    parent2_relation_with_child: Literal['madre','padre','tutora legar','tutor legal','otro']
    parent2_education: str
    parent2_occupation: str
    parent2_phone: str
    parent2_email: str
    # parent2_signature: Signature
    parent2_city: str
    parent2_signature: str
    parent2_date: str = date.today().strftime('%d-%m-%Y')
    
    enrollment_contact: bool
    
    payer_name: str
    payer_adress: str
    payer_postal_code: str
    payer_city: str
    payer_country: str
    payer_account_number: str # either Swift BIC of 8 or 11 char or IBAN of 24 char starting with ES
    payer_recurrent_payment: bool
    payer_city: str
    payer_signature: str
    payer_date: str = date.today().strftime('%d-%m-%Y')
    
    children = list[Child]
    adult_authorization: bool
    children_authorization: bool 
    
    relation: Literal['padre','madre','tutor','tutora']
    personal_vehicle_authorization: bool
    
    conditions: bool
    ongoing_conditions: str = ''
    hospitalized: bool
    why_hospitalized: str = ''
    
    allergies: bool
    allergies_manifestations: str = ''
    allergies_triggers: str = ''
    allergies_treatment: str = ''
    allergies_comments: str = ''
    
    intolerances: bool
    intolerances_comments: str = ''
    
    tetanos_vaccine: bool
    vaccines_comments: str = ''

    professional_contact_name: str  = ''
    professional_contact_number: str = ''
    family_contact_name: str
    family_contact_number: str
    family_contact2_name: str = ''
    family_contact2_number: str = ''
        
    important_info_comments: str = ''
    
    DNI_image: Image
    libro_familia: Image
    tarjeta_sanitaria: Image
    
    
    