from django.urls import path, include
from . import views


app_name = 'school_site'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('my-profile', views.MyProfile.as_view(), name='my_profile'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('my-children-activities', views.ChildrenActivities.as_view(), name='children_activities'),
    path('my-activities', views.MyActivities.as_view(), name='my_activities'),
    path('my-bills', views.MyBills.as_view(), name='my_bills'),
    path('test', views.table_form, name='test_table'),
]
