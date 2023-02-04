from django import forms

YEAR_CHOICES = [(i, str(i)) for i in range(2022, 20122)]

MONTH_CHOICES = [(i, str(i)) for i in range(1, 13)]


class GetMonthlyBillsForm(forms.Form):
    """
    to be used for the view
    """
    year = forms.ChoiceField(required=False, label='year', choices=YEAR_CHOICES)
    month = forms.ChoiceField(required=False, label='month', choices=MONTH_CHOICES)

