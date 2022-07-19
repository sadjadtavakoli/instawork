from http import HTTPStatus

from django.urls import reverse_lazy, reverse

from members.models import Member
from members.tests.test_member_base import MemberTestCase


class MemberListViewTest(MemberTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse_lazy('members:list')

    def main_page_redirect_here(self):
        response = self.client.get(reverse_lazy('main'))
        self.assertRedirects(response, self.url)

    def test_get_list_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Team members')
        self.assertContains(response, 'You have 0 team members.')
        member = Member.objects.create(**self.member1_data)
        response = self.client.get(self.url)
        self.assertContains(response, 'You have 1 team members.')
        self.assertContains(response, reverse('members:edit', args=[member.id]))
        self.assertQuerysetEqual(response.context_data['members'],
                                 Member.objects.order_by('-date_joined').exclude(is_superuser=True))

        member = Member.objects.create(**self.member2_data)
        response = self.client.get(self.url)
        self.assertContains(response, 'You have 2 team members.')
        self.assertContains(response, reverse('members:edit', args=[member.id]))
        self.assertQuerysetEqual(response.context_data['members'],
                                 Member.objects.order_by('-date_joined').exclude(is_superuser=True))

        Member.objects.get(pk=member.id).delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'You have 1 team members.')
        self.assertNotContains(response, reverse('members:edit', args=[member.id]))
