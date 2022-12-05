from django import forms
from v1.models import Parent


def get_parents_list():
    return [(parent.id, parent) for parent in Parent.objects.all()]


class AddPartnerForm(forms.Form):
    """
    to be used for the view
    """
    is_partner_already_created = forms.BooleanField(required=False, label='Choose my partner within the users list', initial=True)
    user = forms.ChoiceField(required=False, label='Parents list', choices=get_parents_list)
    first_name = forms.CharField(required=False, label='Nombre', max_length=15)
    last_name = forms.CharField(required=False, label='Apellidos', max_length=15)
