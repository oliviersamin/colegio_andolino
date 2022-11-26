import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import generic, View
from django.contrib.auth.models import User
from .forms.double_entry_table import BaseTable
from v1.models import Child, Parent, Activity, Sheet, External, Archive

from school_site.utils import (
    parse_checkboxes,
    users_and_dates_for_sheet_table,
    get_current_month_dates_headers,
)

from school_site.forms import (
    ProfileForm,
    MyActivity,
    AddUserAndChild,
    EditChildForm,
    CreateSheetForm,
    EditActivityUsers,
)

from school_site.utils import (
    update_username_with_form,
    set_initial_fields_profile_form,
    get_children_instance_from_form_field,
    update_children_fields_profile_form,
    update_group_fields_profile_form,
    get_group_instance_from_form_field,
    get_parents_instance_from_form_field,
    set_initial_child_fields,
    create_user_from_child_form,
    create_child_from_new_user,
    set_initial_activity_fields,
    save_activity_form_fields,
    set_initial_sheet_fields,
    get_activities_for_actual_school_year,
)


class Home(View):
    """ create the home page before login """
    template_name = 'school_site/home.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context=context)


class Dashboard(View):
    """ access the user's dashboard when logged in """
    template_name = 'school_site/dashboard.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class EditProfile(View):
    """ Edit the user profile to see / modify fields"""
    template_name = 'school_site/edit_profile.html'

    def get(self, request, user_id):
        if request.user.is_authenticated:
            context = {}
            user = User.objects.get(id=user_id)
            parent = Parent.objects.get(user=user)
            dict_initial = set_initial_fields_profile_form(user=user, parent=parent)
            form = ProfileForm(request.POST or None, initial=dict_initial)
            context['form'] = form
            context['children'] = parent.child()
            context['parent'] = parent
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, user_id):
        form = ProfileForm(request.POST)
        success_message = 'Your profile has been updated successfully'
        error_messages = [
            'At least one field of the form has not the proper input',
            'Your profile has not been updated'
        ]
        if form.is_valid():
            username_fields = [
                'first_name',
                'last_name',
            ]
            parent_fields = [
                'phone',
                'mobile',
                'address',
                # 'children',
                'school_status',
                # 'groups',
                'school_email',
                'bank_account',
                'is_paying_bills'
            ]
            many_to_many_fields = ['children', 'group']
            user = User.objects.get(id=user_id)
            parent = Parent.objects.get(user__username=user.username)
            for key, value in form.cleaned_data.items():
                if (key in username_fields) & (value != ''):
                    setattr(user, key, form.cleaned_data[key])
                    user.username = update_username_with_form(user.first_name, user.last_name)
                # if form.cleaned_data['email']:
                #     user.email = form.cleaned_data['email']
                elif key == 'email':
                    setattr(user, key, value)
                elif key in parent_fields:
                    setattr(parent, key, value)
                elif key in many_to_many_fields:
                    if key == 'children':
                        new_data = get_children_instance_from_form_field(value)
                        update_children_fields_profile_form(parent=parent, field=key, new_data=new_data)
                    elif key == 'group':
                        new_data = get_group_instance_from_form_field(value)
                        update_group_fields_profile_form(parent=parent, field=key, new_data=new_data)
                user.save()
                parent.save()
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            for message in error_messages:
                messages.add_message(request, messages.ERROR, message)
        return redirect('school_site:children_activities')


class MyFamily(View):
    """ access the children's user activities """
    template_name = 'school_site/my_family.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            parent = Parent.objects.get(user=request.user)
            partner = parent.partner
            children = parent.children.all()
            # context['my_children'] = children
            # context['activities'] = [{'child': child, 'activities': child.user.activities.all()} for child in children]
            context['children'] = [{'child': child, 'activities': child.user.activities.all()} for child in children]
            context['adults'] = [
                {'user': parent, 'role': 'parent', 'activities': parent.user.activities.all()},
                {'user': partner,  'role': 'partner', 'activities': partner.user.activities.all()},
            ]

            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class AddChild(View):
    template_name = 'school_site/add_child.html'
    form = AddUserAndChild

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            context['form'] = self.form
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request):
        form = AddUserAndChild(request.POST)
        date_format = '%Y-%m-%d'
        if form.is_valid():
            user = create_user_from_child_form(form)
            child = create_child_from_new_user(form, user)
            parent = Parent.objects.get(user=request.user)
            parent.children.add(child)
            parent.save()
            return redirect('school_site:validation_success')
        else:
            for key, value in form.errors.items():
                print('the field "{}" has the following error: {}'.format(key, value.data[0].messages[0]))
            return redirect('school_site:validation_error')


class EditChild(View):
    template_name = 'school_site/edit_child.html'

    def get(self, request, child_id):
        if request.user.is_authenticated:
            user = request.user
            child = Child.objects.get(pk=child_id)
            context = {}
            dict_initial = set_initial_child_fields(child=child)
            form = EditChildForm(request.POST or None, initial=dict_initial)
            context['form'] = form
            context['child'] = child
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, child_id):
        form = EditChildForm(request.POST)
        success_message = 'Your child profil has been updated successfully'
        error_messages = [
            'At least one field of the form has not the proper input',
            'Your child profile has not been updated'
        ]
        date_format = '%Y-%m-%d'
        if form.is_valid():
            child = Child.objects.get(pk=child_id)
            last_names = form.cleaned_data['last_name'].split(' ')
            username = [form.cleaned_data['first_name']] + last_names
            username = '.'.join(username).lower()
            if username != child.user.username:
                child.user.delete()
                user = create_user_from_child_form(form)
                child = create_child_from_new_user(form, user)
                parent = Parent.objects.get(user=request.user)
                parent.children.add(child)
                parent.save()
                messages.add_message(request, messages.SUCCESS, success_message)
            else:
                if child.birth_date != form.cleaned_data['birth_date']:
                    child.birth_date = form.cleaned_data['birth_date']
                    child.save()
                    messages.add_message(request, messages.SUCCESS, success_message)
        else:
            for message in error_messages:
                messages.add_message(request, messages.ERROR, message)

        return redirect('school_site:children_activities')


class MyActivities(View):
    """ access the user activities """
    template_name = 'school_site/my_activities.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            queryset = Activity.objects.filter(creator=request.user)
            context['my_activities'] = queryset
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class CreateMyActivity(View):
    template_name = 'school_site/create_my_activity.html'
    form = MyActivity

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            user = request.user
            # parent = Parent.objects.get(user=user)
            form = self.form(request.POST or None)
            context['form'] = form
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request):
        form = MyActivity(request.POST)
        success_message = 'The activity has been successfully created'
        error_messages = [
            'At least one field of the form has not the proper input',
            'The activity has not been created'
        ]
        if form.is_valid():
            activity = form.save(commit=False)
            activity.creator = request.user
            activity.save()
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            for message in error_messages:
                messages.add_message(request,messages.ERROR, message)
        return redirect('school_site:my_activities')


class EditActivity(View):
    template_name = 'school_site/edit_activity.html'
    form = MyActivity

    def get(self, request, activity_id):
        if request.user.is_authenticated:
            user = request.user
            activity = Activity.objects.get(pk=activity_id)
            context = {}
            dict_initial = set_initial_activity_fields(activity=activity)
            form = self.form(request.POST or None, initial=dict_initial)
            context['form'] = form
            context['activity'] = activity
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, activity_id):
        form = self.form(request.POST)
        date_format = '%Y-%m-%d'
        success_message = 'The activity has been successfully updated'
        error_messages = [
            'At least one field of the form has not the proper input',
            'The activity has not been updated'
        ]
        if form.is_valid():
            activity = Activity.objects.get(pk=activity_id)
            save_activity_form_fields(form, activity)
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            for message in error_messages:
                messages.add_message(request, messages.ERROR, message)
        return redirect('school_site:my_activities')


class EditActivityUsers(View):
    template_name = 'school_site/edit_activity_users.html'
    form = EditActivityUsers

    def get(self, request, activity_id):
        if request.user.is_authenticated:
            user = request.user
            activity = Activity.objects.get(pk=activity_id)
            context = {
                'parents': Parent.objects.all(),
                'children': Child.objects.all(),
                'activity': activity
            }
            # dict_initial = set_initial_activity_users_fields(activity=activity, public=activity.public)
            form = self.form(request.POST or None)  # , initial=dict_initial)
            context['form'] = self.form
            context['activity'] = activity
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, activity_id):
        form = self.form(request.POST)
        success_message = 'The activity users have been successfully updated'
        error_messages = [
            'At least one field of the form has not the proper input',
            'The activity users have not been updated'
        ]
        if form.is_valid():
            activity = Activity.objects.get(pk=activity_id)
            if activity.public == 'parents':
                parents_id = []
                for parent in form.cleaned_data['parents']:
                    parents_id.append(parent.user.id)
                activity.users.set(parents_id)
            else:
                children_id = []
                for child in form.cleaned_data['children']:
                    children_id.append(child.user.id)
                activity.users.set(children_id)
            activity.save()
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            for message in error_messages:
                messages.add_message(request, messages.ERROR, message)
        return redirect('school_site:my_activities')


class CreateSheet(View):
    template_name = 'school_site/create_sheet.html'
    form = CreateSheetForm

    @staticmethod
    def is_this_school_year_date(year, month):
        now = datetime.datetime.now()
        if year == now.year:
            if now.month in range(9, 13):
                if month in range(9, 13):
                    return True
                return False
            elif now.month in range(1, 7):
                if month in range(1, 7):
                    return True
                return False
        elif year == now.year + 1:
            if month in range(1, 7):
                return True
            return False
        elif year == now.year - 1:
            if month in range(9, 13):
                return True
            return False
        return False

    def get(self, request, activity_id):
        if request.user.is_authenticated:
            context = {}
            context['form'] = self.form
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, activity_id):
        form = self.form(request.POST)
        success_message = 'The sheet has been successfully created'
        error_message_already_existing = 'This sheet already exists'
        error_message_dates_error = [
            'Only actual school dates can be used to create sheets',
            'The sheet has not been created'
        ]
        if form.is_valid():
            # validation to be sure no other sheet has already been created and saved for this activity year and month
            existing_sheet = Sheet.objects.filter(
                year=form.cleaned_data['year']).filter(
                month=form.cleaned_data['month']).filter(activity_id=activity_id).first()
            if not existing_sheet:
                if self.is_this_school_year_date(form.cleaned_data['year'], form.cleaned_data['month']):
                    new_sheet = Sheet()
                    new_sheet.year = form.cleaned_data['year']
                    new_sheet.month = form.cleaned_data['month']
                    new_sheet.activity_id = activity_id
                    new_sheet.content = {}
                    new_sheet.save()
                    messages.add_message(request, messages.SUCCESS, success_message)
                else:
                    for message in error_message_dates_error:
                        messages.add_message(request, messages.ERROR, message)
            elif existing_sheet:
                messages.add_message(request, messages.ERROR, error_message_already_existing)
        return redirect('school_site:my_activities')


class EditSheet(View):
    template_name = 'school_site/edit_sheet.html'
    form = CreateSheetForm
    def get(self, request, sheet_id):
        if request.user.is_authenticated:
            headers_column, rows = users_and_dates_for_sheet_table(sheet_id)
            sheet = Sheet.objects.get(id=sheet_id)
            activity = sheet.activity
            title = 'Activity: {} - Creator: {} - Year: {} - Month: {}'.format(
                activity.name,
                activity.creator.get_full_name(),
                sheet.year,
                sheet.month
            )
            dict_initial = set_initial_sheet_fields(sheet)
            form = self.form(request.POST or None, initial=dict_initial)
            context = {
                'headers_column': headers_column,
                'rows': rows,
                'form': form,
                'title': title,
                'selected_buttons': dict_initial['content']
            }
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, sheet_id):
        form = self.form(request.POST)
        success_message = 'The sheet has been successfully updated'
        error_messages = [
            'At least one field of the form has not the proper input',
            'The sheet has not been updated'
        ]
        if form.is_valid():
            content = parse_checkboxes(request)[2:]
            # activity = Activity.objects.get(pk=activity_id)
            sheet = Sheet.objects.get(id=sheet_id)
            sheet.year = form.cleaned_data['year']
            sheet.month = form.cleaned_data['month']
            sheet.activity_id = sheet.activity_id
            sheet.content = {'on': content}
            sheet.save()
            messages.add_message(request, messages.SUCCESS, success_message)
        else:
            messages.add_message(request, messages.ERROR, error_messages)
        return redirect('school_site:my_activities')


class AskValidateSheet(View):
    template_name = 'school_site/ask_validate_sheet.html'

    def get(self, request, sheet_id):
        if request.user.is_authenticated:
            headers_column, rows = users_and_dates_for_sheet_table(sheet_id)
            sheet = Sheet.objects.get(id=sheet_id)
            activity = sheet.activity
            title = 'Activity: {} - Creator: {} - Year: {} - Month: {}'.format(
                activity.name,
                activity.creator.get_full_name(),
                sheet.year,
                sheet.month
            )
            dict_initial = set_initial_sheet_fields(sheet)
            context = {'sheet_id': sheet_id}
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class ValidateSheet(View):
    def get(self, request, sheet_id):
        """
        1. is archive with month & year of the sheet existing
            a. if not create one
        2. add this sheet the corresponding archive

        """
        success_message = [
            'The sheet has been successfully validated',
            'The sheet is now archived and is not accessible anymore'
        ]
        error_messages = ['The sheet users has not been validated']
        if request.user.is_authenticated:
            sheet = Sheet.objects.get(id=sheet_id)
            try:
                archive = Archive.objects.filter(year=sheet.year).filter(month=sheet.month).first()
                if not archive:
                    archive = Archive()
                    archive.year = sheet.year
                    archive.month = sheet.month
                    archive.save()
                sheet.archive = archive
                sheet.is_archived = True
                sheet.save()
                for message in success_message:
                    messages.add_message(request, messages.SUCCESS, message)
            except Exception as e:
                error_messages.append(e)
                for message in error_messages:
                    messages.add_message(request, messages.ERROR, message)
            return redirect('school_site:my_activities')
        return redirect('school_site:home')


class AskDeleteSheet(View):
    template_name = 'school_site/ask_delete_sheet.html'

    def get(self, request, sheet_id):
        if request.user.is_authenticated:
            context = {
                'sheet_id': sheet_id
            }
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class DeleteSheet(View):
    def get(self, request, sheet_id):
        success_message = 'The sheet has been successfully deleted'
        error_messages = ['The sheet users has not been validated']
        if request.user.is_authenticated:
            try:
                sheet = Sheet.objects.get(pk=sheet_id)
                sheet.delete()
                messages.add_message(request, messages.SUCCESS, success_message)
            except Exception as e:
                error_messages.append(e)
                for message in error_messages:
                    messages.add_message(request, messages.ERROR, message)
            return redirect('school_site:my_activities')
        return redirect('school_site:home')


class MyBills(View):
    """ access the children's user activities """
    template_name = 'school_site/my_bills.html'

    def get(self, request):
        #TODO: 1. for the request.user get all the activities he has attended or his children or his partner
        # 2. retireve all the data from the sheets archived and format them in the input format of Miguel
        """
        For the GET method info I need are:
        1. for each member of the family (parent, parent.partner and children) all the activities they are user
        for the whole school year
        """
        if request.user.is_authenticated:
            context = {}
            user_activities = get_activities_for_actual_school_year(request.user)
            parent = Parent.objects.get(user=request.user)
            partner_activities = get_activities_for_actual_school_year(parent.partner.user)
            children_activities = [get_activities_for_actual_school_year(child.user) for child in parent.children.all()]
            activities = Activity.objects.all()
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request):
        """
        For now the output format of the POST method will be:
        [{
        'user': 'Olivier',
        'activities': [{
                        'name': 'judo',
                        'year': 2022,
                        'month': 11,
                        'participation_dates': [1, 3, 6, 28]
                        }, {'name': 'musica', 'year': 2022, 'month': 11, ....}, ...]
        },
        'user': 'Paula',
        'activities': [{ ... }]}, ....]
        """
        pass

