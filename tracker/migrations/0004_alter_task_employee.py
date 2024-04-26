# Generated by Django 5.0.4 on 2024-04-26 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_employee_owner_task_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.employee', verbose_name='Выполняющий задачу сотрудник'),
        ),
    ]
