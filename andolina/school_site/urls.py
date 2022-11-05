from django.urls import path, include
from . import views


app_name = 'school_site'

urlpatterns = [
    path('', views.table_form, name='table_form')
]
