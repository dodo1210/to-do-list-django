# Generated by Django 3.0.3 on 2020-03-01 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_maintasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintasks',
            name='task',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Tarefa', to='core.Tasks'),
        ),
    ]
