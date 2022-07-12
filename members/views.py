# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView

from members.forms import AddMemberForm
from members.models import Member


class MemberListView(ListView):
    template_name = 'members/member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        return Member.objects.order_by('-date_joined')


class CreateMemberView(CreateView):
    model = Member
    template_name = 'members/add_member.html'
    form_class = AddMemberForm

    def get_success_url(self):
        return reverse('members:list')


class UpdateMemberView(UpdateView):
    model = Member
    template_name = 'members/edit_member.html'
    form_class = AddMemberForm

    def get_success_url(self):
        return reverse('members:list')
