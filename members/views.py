# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from members.models import Member


class MemberListView(ListView):
    template_name = 'members/member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        return Member.objects.order_by('-date_joined')


class CreateMemberView(CreateView):
    model = Member
    template_name = 'members/edit_member.html'
    fields = ['first_name', 'last_name', 'email', 'phone']

    def get_success_url(self):
        return reverse('members:list')


class MemberDetailView(DetailView):
    model = Member
    template_name = 'members/member_details.html'


class UpdateMemberView(UpdateView):
    model = Member
    template_name = 'members/edit_member.html'
    fields = ['first_name', 'last_name', 'email', 'phone']
