from django import forms
from v1.models import Child
from v1.constants import (
    SCHOOL_STATUS,
    SCHOOL_GROUPS,
)


def get_children():
    return [(child, child.display_user_details()) for child in Child.objects.all()]



class ProfileForm(forms.Form):
    # CHILDREN = [(child, child.display_user_details()) for child in Child.objects.all()]
    first_name = forms.CharField(required=False, label='Nombre', max_length=15)
    last_name = forms.CharField(required=False, label='Apellidos', max_length=15)
    email = forms.EmailField(required=False, label='Personal email', help_text='direccion de correo electronico personal')
    phone = forms.CharField(required=False, label='Telefono', max_length=15)
    mobile = forms.CharField(required=False, label='Movil', max_length=15)
    address = forms.CharField(max_length=200, required=False, label='Direccion', help_text="Poner la direccion completa")
    children = forms.MultipleChoiceField(required=False, label='My children', choices=get_children, help_text="ejemplo por 2 niños: Gabrielle.SAMIN.GONZALEZ,Toto.SAMIN.GONZALEZ")
    school_status = forms.ChoiceField(required=False, label='Estatus', choices=SCHOOL_STATUS)
    group = forms.MultipleChoiceField(required=False, label='Circulos', choices=SCHOOL_GROUPS)
    school_email = forms.EmailField(required=False, label='Email de la escuela', help_text='direccion de correo electronico de la escuela')
    nif = forms.CharField(required=False, label='NIF', max_length=15)
    bank_account = forms.CharField(max_length=50, required=False, label='Cuenta bancaria', help_text='pone tu cuenta bancaria para pagar la escuela')
    is_paying_bills = forms.BooleanField(required=False, label='Pagas facturas?', help_text='Eres tu que pagas las facturas?')

    def get_all_fields_names_and_values(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'address': self.address,
            'children': self.children,
            'school_status': self.school_status,
            'groups':self.groups,
            'school_email': self.school_email,
            'bank_account': self.bank_account,
            'is_paying_bills': self.is_paying_bills
        }
