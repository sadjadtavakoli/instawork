# Generated by Django 4.0.6 on 2022-07-16 07:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be formatted as ###-###-####.', regex='^\\d{3}[-]\\d{3}[-]\\d{4}$')], verbose_name='phone'),
        ),
    ]
