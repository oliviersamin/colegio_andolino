from django import forms


class CreateSheetForm(forms.Form):
    year = forms.IntegerField(required=True, label='year', help_text='year the activity takes place')
    month = forms.IntegerField(required=True, label='month', help_text='month number between 1 and 12')


