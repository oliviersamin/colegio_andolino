from django.contrib import admin
from v1.models import (
    Parent,
    Child,
    Teacher,
    Group,
    Document
)
from django.contrib import messages
from rest_framework import filters
from django.contrib.auth.models import User


class ParentAdmin(admin.ModelAdmin):
    """ Implemented to use parent model from database """
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'children']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'children')
    list_display = ('last_name', 'first_name', 'child', 'school_status', 'mobile', )

    # def get_queryset(self, request):
    #     return super().get_queryset(request)

    # def message_user(self, *args):
    #     """
    #     override this method to cancel all the usual messages displayed when clicked on the save button
    #     :param args:
    #     :return:
    #     """
    #     pass

    # def save_model(self, request, obj, form, change):
    #     """
    #     Step 1: check if there are contracts (even not signed) with this client.
    #     Step 2: any superuser can change anything anytime about the client
    #     Step 3: if there are not, then any sales can change the client details
    #     Step 4: if there are, then only the sales that have signed contracts can change the client details
    #     :param request:
    #     :param obj:
    #     :param form:
    #     :param change:
    #     :return:
    #     """
    #     # Step 1
    #     existing_contracts = list(Contract.objects.filter(client_id=obj.client_id))
    #     existing_contracts = [contract.sales.user for contract in existing_contracts]
    #     # Step 2
    #     if request.user.is_superuser:
    #         super().save_model(request, obj, form, change)
    #         if not change:
    #             message = "Client créé avec succès"
    #         else:
    #             message = "Client modifié avec succès"
    #         messages.success(request, message)
    #     # Step 3
    #     elif not change:
    #         super().save_model(request, obj, form, change)
    #         message = "Client créé avec succès"
    #         messages.success(request, message)
    #     # Step 4
    #     else:
    #         if (existing_contracts != []) & (request.user in existing_contracts):
    #             super().save_model(request, obj, form, change)
    #             message = "Client modifié avec succès"
    #             messages.success(request, message)
    #         elif (request.user not in existing_contracts) & (existing_contracts != []):
    #             message = "Vous n'êtes pas autorisé à modifier les détails de ce client car " \
    #                       "vous n'avez signé aucun contrat avec lui."
    #             messages.error(request, message)
    #         else:
    #             super().save_model(request, obj, form, change)
    #             message = "Client modifié avec succès"
    #             messages.success(request, message)


class ChildAdmin(admin.ModelAdmin):
    """ Implemented to use child model from database """
    search_fields = ['user.first_name', 'user.last_name', 'birth_date']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('age', 'user')
    list_display = ('display_user_details', 'get_age', 'parents')


class TeacherAdmin(admin.ModelAdmin):
    """ Implemented to use teacher model from database """
    search_fields = ['user.first_name', 'user.last_name', 'pupils']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'pupils')
    list_display = ('last_name', 'first_name', 'pupils')


class GroupAdmin(admin.ModelAdmin):
    """ Implemented to use group model from database """
    search_fields = ['leader', 'representative', 'members', 'name']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('leader', 'representative', 'members', 'name')
    list_display = ('leader', 'representative', 'group_members', 'name')


class DocumentAdmin(admin.ModelAdmin):
    """ Implemented to use document model from database """
    search_fields = ['title', 'creator', 'type', 'date_created', 'type_creation']
    filter_backends = (filters.SearchFilter,)
    list_filter = ('title', 'created_by', 'type', 'date_created', 'type_creation')
    list_display = ('title', 'creator', 'type', 'date_created', 'type_creation')


admin.site.register(Parent, ParentAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Document, DocumentAdmin)
