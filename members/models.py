from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from utils import phone_number_regex


class MemberManager(BaseUserManager):
    """
    Custom Member model manager where email is the unique identifiers
    for authentication instead of usernames
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Member(AbstractUser):
    class RoleChoices(TextChoices):
        admin = 'Admin', _('Admin - Can delete members')
        regular = 'Regular', _('Regular - Can\'t delete members')

    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=30, validators=[phone_number_regex], unique=True)
    role = models.CharField(_('role'), max_length=20, choices=RoleChoices.choices, default=RoleChoices.regular)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MemberManager()

    @property
    def is_admin(self):
        return self.role == self.RoleChoices.admin
