# Generated by Django 4.0.6 on 2022-07-16 10:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_member_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be formatted as ###-###-####.', regex='^\\d{3}[-]\\d{3}[-]\\d{4}$')], verbose_name='phone'),
        ),
    ]
