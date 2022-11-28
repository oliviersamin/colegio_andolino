from django import forms


BILL_USERS_CHOICES = [
    ('My whole family', 'My whole family'),
    ('All my children', 'All my children'),
    ('Only my children', 'Only my children'),
    ('Each of my children', 'Each of my children'),
    ('Only my partner', 'Only my partner'),
    ('Only me', 'Only me'),
    ('My partner and myself', 'My partner and myself')
]

YEAR_CHOICES = [(i, str(i)) for i in range(2022, 20122)]

MONTH_CHOICES = [(i, str(i)) for i in range(1, 13)]


class GenerateBillForm(forms.Form):
    """
    to be used for the view
    """
    users = forms.ChoiceField(required=True, label='Bill for', choices= BILL_USERS_CHOICES)
    whole_actual_school_year = forms.BooleanField(required=True, label='Whole actual school year')
    year = forms.ChoiceField(required=False, label='year', choices=YEAR_CHOICES)
    month = forms.ChoiceField(required=False, label='month', choices=MONTH_CHOICES)

