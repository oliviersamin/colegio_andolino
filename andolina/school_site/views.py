from django.shortcuts import redirect, render
from .forms.double_entry_table import BaseTable
from v1.models import Child
from school_site.utils import (
    parse_checkboxes,
    children_and_dates,
)


def table_form(request):
    form = BaseTable(request.POST or None)
    if request.method == 'POST':
        boxes = parse_checkboxes(request)
        return redirect('home')

    table_column_headers, table_rows = children_and_dates()
    context = {
        'form': form,
        'table_column_headers': table_column_headers,
        'table_rows': table_rows,
    }

    return render(request, 'school_site/double_entry_table.html', context)
