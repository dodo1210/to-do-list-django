# Generated by Django 3.0.3 on 2020-02-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200227_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='title',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
