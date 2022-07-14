# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from rest_framework.generics import DestroyAPIView

from members.forms import AddMemberForm
from members.models import Member
from members.permissions import DeleteMemberPermission


class MemberListView(ListView):
    template_name = 'members/member_list.html'
    context_object_name = 'members'
    queryset = Member.objects.order_by('-date_joined')


class CreateMemberView(CreateView):
    model = Member
    template_name = 'members/add_member.html'
    form_class = AddMemberForm
    success_url = reverse_lazy('members:list')


class UpdateMemberView(UpdateView):
    model = Member
    template_name = 'members/edit_member.html'
    form_class = AddMemberForm
    success_url = reverse_lazy('members:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs['pk']
        return context


class DeleteMemberAPIView(DestroyAPIView):
    permission_classes = [DeleteMemberPermission]
    queryset = Member.objects.all()
