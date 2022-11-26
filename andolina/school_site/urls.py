from django.urls import path, include
from . import views


urlpatterns = [
    # home page before login
    path('', views.Home.as_view(), name='home'),
    # pages after login
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('profile/edit/<int:user_id>', views.EditProfile.as_view(), name='edit_profile'),
    path('my-family', views.MyFamily.as_view(), name='children_activities'),
    path('add-child', views.AddChild.as_view(), name='add_child'),
    path('edit-child/<int:child_id>', views.EditChild.as_view(), name='edit_child'),
    path('my-activities', views.MyActivities.as_view(), name='my_activities'),
    path('create-my-activity', views.CreateMyActivity.as_view(), name='create_my_activity'),
    path('edit-activity/<int:activity_id>', views.EditActivity.as_view(), name='edit_activity'),
    path('edit-activity-users/<int:activity_id>', views.EditActivityUsers.as_view(), name='edit_activity_users'),
    path('create-sheet/<int:activity_id>', views.CreateSheet.as_view(), name='create_sheet'),
    path('edit-sheet/<int:sheet_id>', views.EditSheet.as_view(), name='edit_sheet'),
    path('ask-validate-sheet/<int:sheet_id>', views.AskValidateSheet.as_view(), name='ask_validate_sheet'),
    path('validate-sheet/<int:sheet_id>', views.ValidateSheet.as_view(), name='validate_sheet'),
    path('ask-delete-sheet/<int:sheet_id>', views.AskDeleteSheet.as_view(), name='ask_delete_sheet'),
    path('delete-sheet/<int:sheet_id>', views.DeleteSheet.as_view(), name='delete_sheet'),
    path('my-bills', views.MyBills.as_view(), name='my_bills'),

]
app_name = 'school_site'

