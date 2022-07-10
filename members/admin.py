from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from members.models import Member


class MemberChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Member
        fields = '__all__'
        field_classes = {"email": EmailField}


class MemberAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""
    form = MemberChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Member, MemberAdmin)
