from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings

USERNAME = settings.ADMIN_USERNAME
PASSWORD = settings.ADMIN_PASSWORD


def create_admin(sender, **kwargs):
    member = sender.get_model('Member')
    try:
        member.objects.get(email=USERNAME)
    except member.DoesNotExist:
        member.objects.create_superuser('{}@instawork'.format(USERNAME), PASSWORD)


class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'

    def ready(self):
        post_migrate.connect(create_admin, sender=self)
