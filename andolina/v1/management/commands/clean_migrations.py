from django.core.management import BaseCommand
import os


class Command(BaseCommand):
    help = "Clean all the migrations file and applying all needed migrations"


    def handle(self, *args, **options):
        """
        1. erase all migration files in v1 app
        2. launch makemigrations
        3. launch migrate
        """
        migrations_dir = 'v1/migrations/'
        migrations = os.listdir(migrations_dir)
        filter_to_keep = '__init__.py'
        [os.system('rm ' + os.path.join(migrations_dir, item)) for item in migrations if item != filter_to_keep]
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        os.system('python manage.py runserver')