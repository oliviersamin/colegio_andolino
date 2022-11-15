import datetime
from django.shortcuts import redirect, render
from django.views import generic, View
from django.contrib.auth.models import User
from .forms.double_entry_table import BaseTable
from v1.models import Child, Parent, Activity, Sheet

from school_site.utils import (
    parse_checkboxes,
    children_and_dates,
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


class MyProfile(View):
    """ access the user's profile """
    template_name = 'school_site/my_profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            user = request.user
            parent = Parent.objects.get(user=user)
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class EditProfile(View):
    """ Edit the user profile to see / modify fields"""
    template_name = 'school_site/edit_profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            user = request.user
            parent = Parent.objects.get(user=user)
            dict_initial = set_initial_fields_profile_form(user=user, parent=parent)
            form = ProfileForm(request.POST or None, initial=dict_initial)
            context['form'] = form
            context['children'] = parent.child()
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request):
        form = ProfileForm(request.POST)
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
            user = request.user
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
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


class ChildrenActivities(View):
    """ access the children's user activities """
    template_name = 'school_site/children_activities.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            parent = Parent.objects.get(user=request.user)
            children = parent.children.all()
            # context['my_children'] = children
            context['activities'] = [{'child': child, 'activities': child.user.activities.all()} for child in children]
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
                return redirect('school_site:validation_success')

            else:
                if child.birth_date != form.cleaned_data['birth_date']:
                    child.birth_date = form.cleaned_data['birth_date']
                    child.save()
                    return redirect('school_site:validation_success')
                return redirect('school_site:children_activities')
        return redirect('school_site:validation_error')


class CreateMyActivity(View):
    template_name = 'school_site/create_my_activity.html'
    form = MyActivity

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            user = request.user
            # parent = Parent.objects.get(user=user)
            form = self.form
            context['form'] = form
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request):
        form = MyActivity(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.creator = Parent.objects.get(user=request.user)
            activity.save()
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


class MyActivities(View):
    """ access the user activities """
    template_name = 'school_site/my_activities.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = {}
            parent = Parent.objects.get(user=request.user)
            queryset = Activity.objects.filter(creator=parent)
            context['my_activities'] = queryset
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


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
        if form.is_valid():
            activity = Activity.objects.get(pk=activity_id)
            save_activity_form_fields(form, activity)
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


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
        date_format = '%Y-%m-%d'
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
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


class CreateSheet(View):
    template_name = 'school_site/create_sheet.html'
    form = CreateSheetForm

    def get(self, request, activity_id):
        if request.user.is_authenticated:
            context = {}
            context['form'] = self.form
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, activity_id):
        form = self.form(request.POST)
        if form.is_valid():
            # activity = Activity.objects.get(pk=activity_id)
            new_sheet = Sheet()
            new_sheet.year = form.cleaned_data['year']
            new_sheet.month = form.cleaned_data['month']
            new_sheet.activity_id = activity_id
            new_sheet.content = {}
            new_sheet.save()
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


class EditSheet(View):
    template_name = 'school_site/edit_sheet.html'
    form = CreateSheetForm
    def get(self, request, sheet_id):
        if request.user.is_authenticated:
            headers_column, rows = users_and_dates_for_sheet_table(sheet_id)
            sheet = Sheet.objects.get(id=sheet_id)
            activity = sheet.activity
            title = 'Presential sheet for '
            subtitle = activity.name + ' - ' + activity.creator.user.get_full_name() + '/n' + str(sheet.year) + ' - ' + str(sheet.month)
            dict_initial = set_initial_sheet_fields(sheet)
            form = self.form(request.POST or None, initial=dict_initial)
            context = {
                'headers_column': headers_column,
                'rows': rows,
                'form': form,
                'title': title + subtitle,
                'selected_buttons': dict_initial['content']
            }
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, sheet_id):
        form = self.form(request.POST)
        if form.is_valid():
            content = parse_checkboxes(request)[2:]
            # activity = Activity.objects.get(pk=activity_id)
            sheet = Sheet.objects.get(id=sheet_id)
            sheet.year = form.cleaned_data['year']
            sheet.month = form.cleaned_data['month']
            sheet.activity_id = sheet.activity_id
            sheet.content = {'on': content}
            sheet.save()
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


class AddUsersToActivity(View):
    template_name = 'school_site/add_users_to_activity.html'
    form = CreateSheetForm

    def get(self, request, sheet_id):
        if request.user.is_authenticated:
            headers_column, rows = users_and_dates_for_sheet_table(sheet_id)
            sheet = Sheet.objects.get(id=sheet_id)
            activity = sheet.activity
            title = 'Presential sheet for '
            subtitle = activity.name + ' - ' + activity.creator.user.get_full_name() + '/n' + str(sheet.year) + ' - ' + str(sheet.month)
            dict_initial = set_initial_sheet_fields(sheet)
            form = self.form(request.POST or None, initial=dict_initial)
            context = {
                'headers_column': headers_column,
                'rows': rows,
                'form': form,
                'title': title + subtitle,
                'selected_buttons': dict_initial['content']
            }
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')

    def post(self, request, sheet_id):
        form = self.form(request.POST)
        if form.is_valid():
            content = parse_checkboxes(request)[2:]
            # activity = Activity.objects.get(pk=activity_id)
            sheet = Sheet.objects.get(id=sheet_id)
            sheet.year = form.cleaned_data['year']
            sheet.month = form.cleaned_data['month']
            sheet.activity_id = sheet.activity_id
            sheet.content = {'on': content}
            sheet.save()
            return redirect('school_site:validation_success')
        return redirect('school_site:validation_error')


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
        if request.user.is_authenticated:
            try:
                sheet = Sheet.objects.get(pk=sheet_id)
                sheet.delete()
                return redirect('school_site:validation_success')
            except Exception as e:
                print(e)
                return redirect('school_site:validation_error')
        return redirect('school_site:home')


class MyBills(View):
    """ access the children's user activities """
    template_name = 'school_site/my_bills.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class ValidationFormSuccess(View):
    template_name = 'school_site/success_validation.html'
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class ValidationFormError(View):
    template_name = 'school_site/error_validation.html'
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


def table_form(request):
    # form = BaseTable(request.POST or None)
    # form =
    if request.method == 'POST':
        boxes = parse_checkboxes(request)
        return redirect('home')
    table_column_headers, table_rows = children_and_dates()
    context = {
        'table_column_headers': table_column_headers,
        'table_rows': table_rows,
    }

    return render(request, 'school_site/double_entry_table.html', context)
