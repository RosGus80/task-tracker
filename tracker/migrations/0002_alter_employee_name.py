# Generated by Django 5.0.4 on 2024-04-24 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Имя сотрудника'),
        ),
    ]
