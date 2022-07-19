from http import HTTPStatus

from django.urls import reverse
from django_webtest import WebTestMixin

from members.models import Member
from members.tests.test_member_base import MemberTestCase


class DeleteMemberApiViewTest(WebTestMixin, MemberTestCase):

    def setUp(self):
        super().setUp()
        self.member1_data['password'] = 'password'
        self.member2_data['password'] = 'password'
        self.member1 = Member.objects.create_user(**self.member1_data)
        self.member2 = Member.objects.create_user(**self.member2_data)
        member3_data = self.member2_data
        member3_data.update({'email': 'memeber3@gmail.com', 'phone': '222-888-4466'})
        self.member3 = Member.objects.create(**member3_data)

    def test_delete_with_unauthorized_user(self):
        response = self.client.delete(reverse('members:delete', args=[self.member3.id]))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(Member.objects.filter(pk=self.member3.id).exists())

    def test_delete_with_regular_user(self):
        self.client.force_login(self.member1)
        response = self.client.delete(reverse('members:delete', args=[self.member3.id]))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(Member.objects.filter(pk=self.member3.id).exists())

    def test_delete_with_admin_user(self):
        self.client.force_login(self.member2)
        response = self.client.delete(reverse('members:delete', args=[self.member3.id]))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(Member.objects.filter(pk=self.member3.id).exists())
