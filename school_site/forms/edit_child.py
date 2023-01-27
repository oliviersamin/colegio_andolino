from django import forms


class EditChildForm(forms.Form):
    """
    to be used for the view
    """
    first_name = forms.CharField(required=True, label='Nombre', max_length=15)
    last_name = forms.CharField(required=True, label='Apellidos', max_length=15)
    birth_date = forms.DateField(
        required=True,
        label='birth date',
        help_text='example: 2015-10-27'
    )
