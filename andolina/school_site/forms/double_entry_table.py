from django import forms
from v1.models import Child


class BaseTable(forms.Form):

    ROW_CHOICES = [str(i) for i in range(1, 32)]
    # query = Child.objects.all()
    title = forms.CharField(max_length = 50)
    # rows = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ROW_CHOICES)
    # table_column_headers = [i for i in range(1, 32)]
    # table_row_headers = [child.user.get_full_name() for child in query]
    # table_rows = [{'header': child.user.get_full_name(), 'columns': [str(child.id) + '_' + str(i) for i in range(1, 32)]} for child in query]
    # table_checkbox_names = []
    # for child in query:
    #     table_checkbox_names.append([str(child.id) + '_' + str(i) for i in range(32)])
    # content = {
    #     'column_headers': table_column_headers,
    #     'rows': table_rows,
    # }
    # context = {
    #     'form': form,
    #     'table_column_headers': table_column_headers,
    #     'table_row_headers': table_row_headers,
    #     'table_rows': table_rows,
    # }
