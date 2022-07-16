from django import forms

from members.models import Member


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (###-###-####)'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }
