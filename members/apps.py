from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

EMAIL = settings.ADMIN_EMAIL
PASSWORD = settings.ADMIN_PASSWORD


def create_admin(sender, **kwargs):
    member = sender.get_model('Member')
    try:
        member.objects.get(email=EMAIL)
    except member.DoesNotExist:
        member.objects.create_superuser(EMAIL, PASSWORD)


class MemberConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = 'members'

    def ready(self):
        post_migrate.connect(create_admin, sender=self)
