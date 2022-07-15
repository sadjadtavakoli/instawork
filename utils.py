from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(regex=r'^\d{3}[-]\d{3}[-]\d{4}$',
                                    message='Phone number must be formatted as ###-###-####.')
