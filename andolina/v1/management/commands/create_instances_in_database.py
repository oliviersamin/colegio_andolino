
import time
import datetime
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from v1.utils import Operation
from v1.models import(
    Child,
    Parent,
    Activity,
    Sheet,
)


class Command(BaseCommand):
    help = 'create instances into the database'
    CHILDREN_PATH = '/home/olivier/Documents/Projets/Andolina/colegio_andolino/andolina/v1/raw_data_previous_year/Alumnos.csv'
    COMEDOR_FOLDER_PATH = '/home/olivier/Documents/Projets/Andolina/colegio_andolino/raw_data/clean/Comedor'
    EARLY_CARE_FOLDER_PATH = '/home/olivier/Documents/Projets/Andolina/colegio_andolino/raw_data/clean/AtenciónTemprana'
    ACTIVITIES_PATH = '/home/olivier/Documents/Projets/Andolina/colegio_andolino/andolina/v1/activities.csv'
    ACTIVITIES = [
        {'name': 'Comedor', 'public': 'children', 'path': COMEDOR_FOLDER_PATH},
        {'name': 'Atencion temprana', 'public': 'children', 'path': EARLY_CARE_FOLDER_PATH},
    ]
    birth_date_format = '%Y-%m-%d'
    children_separator = '-'
    sleeping_time = 1
    default_user_password = 'passwd_test'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', type=str, default='all', help='model to create instances from')

    def fetch_data_from_csv(self, csv_path) -> list:
        data = []
        with open(csv_path, 'r') as file:
            data = file.readlines()
        data = [line[:-1].split(',') for line in data]
        return data

    def setup_username_child(self, line):
        name = line[2].lower()
        if len(name.split(' ')) > 1:
            name = '.'.join(name.split(' '))
        surnames = '.'.join(line[3].split(' ')).lower()
        return '.'.join([name, surnames]).lower()

    def setup_username_parents(self, line):
        parent1 = line[4][:-1].lower()
        parent2 = line[5][:-1].lower()
        return {'mother': parent1, 'father': parent2}

    def create_users_instances_from_data(self, line) -> None:
        password = self.default_user_password
        for data in line:
            username_child = self.setup_username_child(data)
            username_parents = self.setup_username_parents(data)
            username_mom = username_parents['mother']
            username_dad = username_parents['father']
            if not User.objects.filter(username=username_child).first():
                user = User.objects.create_user(
                    username=username_child,
                    password=password,
                )
                user.save()
                child = Child()
                child.user = user
                child.save()
                print('new user {} created'.format(username_child))

            child_user = User.objects.filter(username=username_child).first()
            child = Child.objects.get(user=child_user)

            if username_mom != '':
                if not User.objects.filter(username=username_mom).first():
                    user = User.objects.create_user(
                        username=username_mom,
                        password=password,
                    )
                    user.save()
                    parent = Parent()
                    parent.user = user
                    parent.save()
                    parent.children.add(child)
                    parent.save()
                    print('new user {} created'.format(username_mom))

            if username_dad != '':
                if not User.objects.filter(username=username_dad).first():
                    user = User.objects.create_user(
                        username=username_dad,
                        password=password,
                    )
                    user.save()
                    parent = Parent()
                    parent.user = user
                    parent.save()
                    parent.children.add(child)
                    parent.save()
                    print('new user {} created'.format(username_dad))

    def delete_users(self):
        print('-' * 50 + ' delete users ' + '-' * 50)
        users = User.objects.filter(is_superuser=False)
        [user.delete() for user in users]
        print('-' * 50 + ' all users deleted ' + '-' * 50)

    def create_sheet_for_one_month(self, path_file, data_to_send):
        with open(path_file, 'r') as file:
            data = file.readlines()
        headers = data[0].split(',')
        month = headers[1]
        month = int(month[month.find('/') + 1:])
        days = [day[:day.find('/')] for day in headers[1:]]
        content = {'on': []}

        for ind in range(len(data[1:])):
            line = data[ind + 1].replace('\n', '').split(',')
            indices = [i for i, v in enumerate(line[2:]) if v != '']
            last_names = line[0][1:].replace(' ', '.').lower()
            first_names = line[1][1:-1].replace(' ', '.').lower()
            username = '.'.join([first_names, last_names])
            user_id = User.objects.get(username=username).id
            user_content = [str(user_id) + '_' + days[i] for i in indices]
            content['on'] += user_content
        # TODO: create the sheet corresponding and add data using self.create_one_sheet
        data_to_send['month'] = month
        data_to_send['content'] = content
        self.create_one_sheet(data_to_send)

    def create_one_sheet(self, data: dict):
        """
        data = {'activity': activity, 'year': '2023', 'month': '1', 'content': [], 'is_archived': 'yes'}
        """
        print(data)
        if data['month'] > 8:
            year = 2050
        else:
            year = 2051
        sheet = Sheet()
        sheet.activity = data['activity']
        sheet.year = year
        sheet.month = data['month']
        sheet.content = data['content']
        sheet.is_archived = True
        sheet.save()

    def create_activity(self, activity_data):
        """
        STEPS:
        1. create activity
        2. get data
        3. set data in proper way to use for activity sheet
        4. create sheet and archive it
        """
        print('-' * 35 + ' creating activity {} & its sheets... '.format(activity_data['name']) + '-' * 35)
        # CREATE ACTIVITY
        activity = Activity()
        activity.name = activity_data['name']
        # activity.creator = User.objects.get(username='admin')
        activity.public = activity_data['public']
        activity.save()
        activity.ask_inscription.set([User.objects.get(username='admin')])
        activity.save()
        # CREATE SHEETS
        files = os.listdir(activity_data['path'])
        # TODO: for all files
        data_to_send = {'activity': activity}
        for indice, file in enumerate(files):
            if 'total.csv' not in file:
                self.create_sheet_for_one_month(self.COMEDOR_FOLDER_PATH + '/' + file, data_to_send)
        print('-' * 35 + ' activity {} & its sheets created! '.format(activity_data['name']) + '-' * 35)

    def delete_all_activities(self):
        print('-' * 50 + ' delete all activities ' + '-' * 50)
        activities = Activity.objects.all()
        [activity.delete() for activity in activities]
        print('-' * 50 + ' all activities have been deleted' + '-' * 50)

    def create_child_parents_form_csv(self):
        """
        use the children csv file from last year to create children and associated parents
        for each line:
        1. check if the users corresponding to its parents exist. If not created create them as users and then parents
        2. create prof if not existed
        3. create the user for the child
        4. create the child instance from the previous user
        """
        data = self.fetch_data_from_csv(self.CHILDREN_PATH)
        self.create_users_instances_from_data(data[1:])

    def handle(self, *args, **options):
        model = options.get('model').lower()

        if model == 'users':
            self.delete_users()
            self.create_child_parents_form_csv()

        elif model == 'activity':
            self.delete_all_activities()
            for activity in self.ACTIVITIES:
                self.create_activity(activity)

        elif model == 'all':
            self.delete_users()
            self.create_child_parents_form_csv()
            self.delete_all_activities()
            for activity in self.ACTIVITIES:
                self.create_activity(activity)
