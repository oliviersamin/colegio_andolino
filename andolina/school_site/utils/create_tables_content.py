from v1.models import Child

def children_and_dates():
    query = Child.objects.all()
    table_column_headers = [i for i in range(1, 32)]
    table_rows = [{'header': child.user.get_full_name(), 'columns': [str(child.id) + '_' + str(i) for i in range(1, 32)]} for child in query]
    return table_column_headers, table_rows