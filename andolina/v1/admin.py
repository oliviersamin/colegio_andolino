from django.contrib import admin
from v1.models import (
    Parent,
    Child,
    Teacher,
    Group,
    Document,
    Activity,
    Sheet,
    Archive,
    External,
    LimitationPrice,
    MonthlyBills,
)
from django.contrib import messages
from rest_framework import filters
from django.contrib.auth.models import User


class ParentAdmin(admin.ModelAdmin):
    """ Implemented to use parent model from database """
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'children', 'groups']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'children')
    list_display = ('parent_id', 'last_name', 'first_name', 'child', 'school_status', 'mobile', 'groups')


class ChildAdmin(admin.ModelAdmin):
    """ Implemented to use child model from database """
    search_fields = ['user.first_name', 'user.last_name', 'birth_date']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('age', 'user')
    list_display = ('child_id', 'display_user_details', 'get_age', 'parents')


class TeacherAdmin(admin.ModelAdmin):
    """ Implemented to use teacher model from database """
    # search_fields = ['user.first_name', 'user.last_name', 'pupils']
    # filter_backends = (filters.SearchFilter,)
    # list_filter = ('user__first_name', 'user__last_name', 'pupils')
    list_display = ('teacher_id', 'last_name', 'first_name', 'pupils')


class GroupAdmin(admin.ModelAdmin):
    """ Implemented to use group model from database """
    search_fields = ['leader', 'representative', 'members', 'name']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('leader', 'representative', 'members', 'name')
    list_display = ('group_id', 'leader', 'representative', 'group_members', 'name')


class DocumentAdmin(admin.ModelAdmin):
    """ Implemented to use document model from database """
    search_fields = ['title', 'addressee', 'type', 'date_created', 'type_creation']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('title', 'recipient', 'type', 'date_created', 'type_creation')
    list_display = ('document_id', 'title', 'addressee', 'type', 'date_created', 'type_creation')


class ActivityAdmin(admin.ModelAdmin):
    """ Implemented to use document model from database """
    search_fields = ['name', 'date', 'is_all_year', 'public']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('name', 'date', 'is_all_year', 'public')
    list_display = ('name', 'public', 'is_all_year')


class SheetAdmin(admin.ModelAdmin):
    """ Implemented to use document model from database """
    search_fields = ['activity', 'year', 'month']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('activity', 'year', 'month')
    list_display = ('activity', 'year', 'month')


class ArchiveAdmin(admin.ModelAdmin):
    """ Implemented to use document model from database """
    search_fields = ['type', 'year', 'month', 'name']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('type', 'year', 'month', 'name')
    list_display = ('type', 'year', 'month', 'name')


class ExternalAdmin(admin.ModelAdmin):
    """ Implemented to use External model from database """
    search_fields = ['user.first_name', 'user.last_name']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('user__first_name', 'user__last_name')
    list_display = ('external_id', 'full_name')


class LimitationPriceAdmin(admin.ModelAdmin):
    """ Implemented to use External model from database """
    search_fields = ['activity', 'date_created', 'date_updated']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('activity', 'date_created', 'date_updated', 'limit_type')
    list_display = ('activity', 'date_created', 'date_updated')


class MonthlyBillsAdmin(admin.ModelAdmin):
    search_fields = ['date']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('date', )
    list_display = ('date', )


admin.site.register(MonthlyBills, MonthlyBillsAdmin)
admin.site.register(LimitationPrice, LimitationPriceAdmin)
admin.site.register(Archive, ArchiveAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Sheet, SheetAdmin)
admin.site.register(External, ExternalAdmin)
