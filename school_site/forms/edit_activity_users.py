from django import forms
from v1.models import Child, Parent


class EditActivityUsers(forms.Form):
    parents = forms.ModelMultipleChoiceField(blank=True, required= False, queryset=Parent.objects.all())
    children = forms.ModelMultipleChoiceField(blank=True, required= False, queryset=Child.objects.all())


