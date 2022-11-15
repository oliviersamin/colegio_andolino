from django.urls import path, include
from . import views


app_name = 'school_site'

urlpatterns = [
    # home page before login
    path('', views.Home.as_view(), name='home'),
    # pages after login
    path('my-profile', views.MyProfile.as_view(), name='my_profile'),
    path('my-profile/edit', views.EditProfile.as_view(), name='edit_profile'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('my-children-activities', views.ChildrenActivities.as_view(), name='children_activities'),
    path('add-child', views.AddChild.as_view(), name='add_child'),
    path('edit-child/<int:child_id>', views.EditChild.as_view(), name='edit_child'),
    path('my-activities', views.MyActivities.as_view(), name='my_activities'),
    path('create-my-activity', views.CreateMyActivity.as_view(), name='create_my_activity'),
    path('edit-activity/<int:activity_id>', views.EditActivity.as_view(), name='edit_activity'),
    path('edit-activity-users/<int:activity_id>', views.EditActivityUsers.as_view(), name='edit_activity_users'),
    path('create-sheet/<int:activity_id>', views.CreateSheet.as_view(), name='create_sheet'),
    path('edit-sheet/<int:sheet_id>', views.EditSheet.as_view(), name='edit_sheet'),
    path('ask-delete-sheet/<int:sheet_id>', views.AskDeleteSheet.as_view(), name='ask_delete_sheet'),
    path('delete-sheet/<int:sheet_id>', views.DeleteSheet.as_view(), name='delete_sheet'),
    path('my-bills', views.MyBills.as_view(), name='my_bills'),
    path('test', views.table_form, name='test_table'),
    # form validation message pages
    path('success', views.ValidationFormSuccess.as_view(), name='validation_success'),
    path('error', views.ValidationFormError.as_view(), name='validation_error'),

]
