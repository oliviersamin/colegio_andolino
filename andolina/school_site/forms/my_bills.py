from django import forms


BILL_USERS_CHOICES = [
    ('family', 'My whole family'),
    ('children', 'Only my children'),
    ('child', 'Only my child'),
    ('each_child', 'Each of my children'),
    ('partner', 'Only my partner'),
    ('me', 'Only me'),
    ('partner_me', 'My partner and myself')
]

YEAR_CHOICES = [(i, str(i)) for i in range(2022, 20122)]

MONTH_CHOICES = [(i, str(i)) for i in range(1, 13)]


class GenerateBillForm(forms.Form):
    """
    to be used for the view
    """
    users = forms.ChoiceField(required=True, label='Bill for', choices= BILL_USERS_CHOICES)
    whole_actual_school_year = forms.BooleanField(required=False, label='Whole actual school year')
    year = forms.ChoiceField(required=False, label='year', choices=YEAR_CHOICES)
    month = forms.ChoiceField(required=False, label='month', choices=MONTH_CHOICES)

