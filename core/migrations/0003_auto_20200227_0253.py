# Generated by Django 3.0.3 on 2020-02-27 02:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_tesks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tesks',
            new_name='Tasks',
        ),
    ]
