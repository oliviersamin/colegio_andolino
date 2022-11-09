from django.shortcuts import redirect, render
from django.views import generic, View
from .forms.double_entry_table import BaseTable
from v1.models import Child, Parent
from school_site.utils import (
    parse_checkboxes,
    children_and_dates,
)
from school_site.constants import BANNER
from school_site.forms import ProfileForm
from school_site.utils import (
    update_username_with_form,
    set_initial_fields_profile_form,
    get_children_instance_from_form_field,
    update_children_fields_profile_form,
    update_group_fields_profile_form,
    get_group_instance_from_form_field,
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
        context = BANNER
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class MyProfile(View):
    """ access the user's profile """
    template_name = 'school_site/my_profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            context = BANNER
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
            return redirect('school_site:dashboard')


class ChildrenActivities(View):
    """ access the children's user activities """
    template_name = 'school_site/children_activities.html'

    def get(self, request):
        context = BANNER
        if request.user.is_authenticated:
            parent = Parent.objects.get(user=request.user)
            children = parent.children.all()
            context['activities'] = [{'child': child, 'activities': child.user.activities.all()} for child in children]
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class MyActivities(View):
    """ access the children's user activities """
    template_name = 'school_site/my_activities.html'

    def get(self, request):
        context = BANNER
        if request.user.is_authenticated:
            return render(request, self.template_name, context=context)
        return redirect('school_site:home')


class MyBills(View):
    """ access the children's user activities """
    template_name = 'school_site/my_bills.html'

    def get(self, request):
        context = BANNER
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
