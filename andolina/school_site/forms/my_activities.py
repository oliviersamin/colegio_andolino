from django import forms
from v1.models import Activity


class MyActivity(forms.Form):
    PARTICIPANTS = [(activity, activity.name) for activity in Activity.objects.all()]
    name = forms.CharField(required=False, label='Nombre de la actividad', max_length=40)
    users = forms.MultipleChoiceField(required=False, label='participantes', choices=PARTICIPANTS, help_text='participantes a la actividad')
    is_all_year = forms.BooleanField(required=False, label='Too el año?', help_text='Este actividad va a durar todo el año escolar?')
    price_per_day = forms.FloatField(required=False, label='precio al dia', help_text='rellenar solamente si el precio de la actividad no es por mes')
    price_per_month = forms.FloatField(required=False, label='precio al mes', help_text='rellenar solamente si el precio de la actividad es por mes')
    is_for_children = forms.BooleanField(required=False, label='es para niños?', help_text='Este actividad esta para los niños?')
    is_for_parents = forms.BooleanField(required=False, label='es para padres?', help_text='Este actividad esta para los padres?')
    money_earned_by_school = forms.FloatField(required=False, label='dinero ganado por la escuela', help_text='rellenar solamente si dinero se gana por la escuela (loteria de navidad...)')
    date = forms.DateField(required=False, label='fecha', help_text='rellenar solamente si la actividad es ponctual')

    def get_all_fields_names_and_values(self):
        return {
            'name': self.name,
            'users': self.users,
            'is_all_year': self.is_all_year,
            'price_per_day': self.price_per_day,
            'price_per_month': self.price_per_month,
            'is_for_children': self.is_for_children,
            'is_for_parents': self.is_for_parents,
            'money_earned_by_school': self.money_earned_by_school,
            'date':self.date,
        }
