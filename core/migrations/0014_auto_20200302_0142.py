# Generated by Django 3.0.3 on 2020-03-02 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200302_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='main_task',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.MainTasks', verbose_name='Tarefa Principal'),
        ),
    ]
