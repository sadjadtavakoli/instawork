from django.urls import path

from members.views import MemberListView, UpdateMemberView, CreateMemberView

app_name = 'members'

urlpatterns = [
    path('', MemberListView.as_view(), name='list'),
    path('new', CreateMemberView.as_view(), name='new'),
    path('<int:pk>/edit', UpdateMemberView.as_view(), name='edit'),
]
