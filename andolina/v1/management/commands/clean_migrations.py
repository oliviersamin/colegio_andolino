from django.core.management import BaseCommand
import os
from pathlib import Path

class Command(BaseCommand):
    help = "Clean all the migrations file and applying all needed migrations"


    def handle(self, *args, **options):
        """
        1. erase all migration files in v1 app
        2. launch makemigrations
        3. launch migrate
        """
        grandpa = Path(__file__).parents[2]
        migrations_dir = os.path.join(grandpa,'migrations/')
        migrations = os.listdir(migrations_dir)
        filter_to_keep = ['__init__.py', '__pycache__']
        [os.system('rm ' + os.path.join(migrations_dir, item)) for item in migrations if item not in filter_to_keep]
        os.system('python andolina/manage.py makemigrations')
        os.system('python andolina/manage.py migrate')
        os.system('python andolina/manage.py runserver')