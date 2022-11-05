
import time
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from v1.utils import Operation
from v1.models import(
    Child,
    Parent,
    Teacher
)


class Command(BaseCommand):
    help = 'create instances into the database'
    USERS_PATH = '/home/olivier/Documents/Projets/Andolina/colegio_andolino/andolina/v1/users.csv'
    birth_date_format = '%Y-%m-%d'
    children_separator = '-'
    sleeping_time = 1

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='model to create instances from')

    def fetch_data_from_csv(self, csv_path) -> list:
        data = []
        with open(csv_path, 'r') as file:
            data = file.readlines()
        data = [line[:-1].split(',') for line in data]
        return data

    def setup_username(self, user):
        if user[2]:
            return '.'.join(user[:3]).lower()
        else:
            return '.'.join(user[:2]).lower()

    # def create_instance(self, username, info):
    #     print('-' * 50 + username + '-' * 50)
    #     response = Operation(info).execute()
    #     print('code_response = ', response.status_code)
    #     print('response = ', response.content)

    # def create_instance(self, username, info):
    #     print('-' * 50 + username + '-' * 50)
    #     if info['model'] == 'User':
    #         try:
    #
    #         except Exception as e:
    #             print(e)

    def create_user_instance_from_data(self, data) -> None:
        for user in data[1:]:
            username = self.setup_username(user)
            password = user[3]
            first_name = user[0]
            last_name = user[1] + ' ' + user[2] if user[2] else user[1]
            user = user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            print('new user created')

    def create_teacher_from_user(self, data) -> None:
        for user in data[1:]:
            if user[4] == 'teacher':
                username = self.setup_username(user)
                user_id = User.objects.get(username=username).id
                print('-' * 50 + username + '-' * 50)
                teacher = Teacher()
                teacher.user_id = user_id
                teacher.save()
                print('new teacher created')

    def from_birth_date_to_age(self, birth_date: str) -> int:
        now = datetime.datetime.now()
        birth_date = datetime.datetime.strptime(birth_date, self.birth_date_format)
        diff = (now - birth_date).days
        return int(diff)

    def create_child_from_user(self, data) -> None:
        for user in data[1:]:
            if user[4] == 'child':
                birth_date = user[5]
                tutor_username = user[6].lower()
                username = self.setup_username(user)
                print('-' * 50 + username + '-' * 50)
                age = self.from_birth_date_to_age(birth_date)
                user_id = User.objects.get(username=username).id
                tutor = Teacher.objects.get(user__username=tutor_username)
                child = Child()
                child.user_id = user_id
                child.birth_date = birth_date
                child.age = age
                child.tutor = tutor
                child.save()
                print('new child created')

    def create_parent_from_user(self, data):
        for user in data[1:]:
            if user[4] == 'parent':
                username = self.setup_username(user)
                print('-' * 50 + username + '-' * 50)
                user_id = User.objects.get(username=username).id
                children = user[7].split(self.children_separator)
                children = [child.lower() for child in children]
                children = [Child.objects.get(user__username=child) for child in children]
                parent = Parent()
                parent.user_id = user_id
                parent.save()
                [parent.children.add(child) for child in children]
                parent.save()
                print('new parent created')

    def delete_users(self):
        print('-' * 50 + ' delete users ' + '-' * 50)
        users = User.objects.filter(is_superuser=False)
        [user.delete() for user in users]
        print('-' * 50 + ' all users deleted ' + '-' * 50)

    def handle(self, *args, **options):
        #TODO: modify this function to perform all creations at once if needed
        model = options.get('model').lower()
        data = self.fetch_data_from_csv(self.USERS_PATH)

        if model == 'all':
            self.delete_users()
            self.create_user_instance_from_data(data)
            self.create_teacher_from_user(data)
            self.create_child_from_user(data)
            self.create_parent_from_user(data)
