# Generated by Django 3.0.3 on 2020-03-02 03:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_tasks_markup_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='markup_end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Data de Termino'),
        ),
    ]
