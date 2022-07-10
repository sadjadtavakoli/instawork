from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(regex=r'^(\+1)?[0-9]{10}$', message='Phone number should contain 10 digits.')
