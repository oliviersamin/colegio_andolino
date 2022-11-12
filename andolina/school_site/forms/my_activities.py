# from django import forms
from django.forms import ModelForm
from v1.models import Activity, Parent, Child
from school_site.constants import PUBLIC_CHOICE_ACTIVITY_FORM

class MyActivity(ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        exclude = ['users', 'creator']

