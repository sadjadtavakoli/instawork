from http import HTTPStatus

from django.urls import reverse_lazy

from members.models import Member
from members.tests.test_member_base import MemberTestCase


class CreateMemberViewTest(MemberTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse_lazy('members:new')

    def test_get_new_member_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Add Member")

    def test_valid_data(self):
        self.assertEqual(Member.objects.count(), 1)
        response = self.client.post(self.url, data=self.member1_data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse_lazy('members:list'))
        self.assertEqual(Member.objects.count(), 2)
        member = Member.objects.last()
        self.assertEqual(member.first_name, self.member1_data['first_name'])
        self.assertEqual(member.last_name, self.member1_data['last_name'])
        self.assertEqual(member.phone, self.member1_data['phone'])
        self.assertEqual(member.role, self.member1_data['role'])
        self.assertEqual(member.email, self.member1_data['email'])

    def test_invalid_email(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member1_data['email'] = "invalid_email"
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "Enter a valid email address.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_invalid_phone(self):
        self.assertEqual(Member.objects.count(), 1)

        # invalid length
        self.member1_data['phone'] = "1321"
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "Phone number must be formatted as ###-###-####.", count=1)
        self.assertEqual(Member.objects.count(), 1)

        # invalid format
        self.member1_data['phone'] = "1112223344"
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "Phone number must be formatted as ###-###-####.", count=1)
        self.assertEqual(Member.objects.count(), 1)

        self.member1_data['phone'] = "111222334455"
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "Phone number must be formatted as ###-###-####.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_email_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member1_data.pop('email')
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_email_uniqueness(self):
        Member.objects.create(**self.member1_data)
        self.assertEqual(Member.objects.count(), 2)

        self.member2_data['email'] = self.member1_data['email']
        response = self.client.post(self.url, data=self.member2_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "User with this Email address already exists.", count=1)
        self.assertEqual(Member.objects.count(), 2)

    def test_phone_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member1_data.pop('phone')
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_phone_uniqueness(self):
        Member.objects.create(**self.member1_data)
        self.assertEqual(Member.objects.count(), 2)

        self.member2_data['phone'] = self.member1_data['phone']
        response = self.client.post(self.url, data=self.member2_data)
        self.assertContains(response, "error_message", count=1)
        self.assertContains(response, "User with this Phone already exists.", count=1)
        self.assertEqual(Member.objects.count(), 2)

    def test_role_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member1_data.pop('role')
        response = self.client.post(self.url, data=self.member1_data)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_nameless_user(self):
        pass
