# Generated by Django 4.1.2 on 2022-11-12 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0007_alter_child_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheet',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheet', to='v1.activity'),
        ),
    ]
