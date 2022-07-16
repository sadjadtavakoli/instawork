from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from members.models import Member


class MemberTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.client = Client()
        self.member_data = {
            'first_name': 'stacy',
            'last_name': 'bale',
            'phone': '111-111-1111',
            'email': "stacyBale@gmail.com",
            'role': Member.RoleChoices.regular
        }

        self.member2_data = {
            'first_name': 'Jack',
            'last_name': 'Namin',
            'phone': '222-222-2222',
            'email': "JackNamin@gmail.com",
            'role': Member.RoleChoices.admin
        }


class MemberModelTest(MemberTestCase):
    def test_superuser_existence(self):
        self.assertEqual(Member.objects.count(), 1)
        member = Member.objects.first()
        self.assertTrue(member.is_superuser)
        self.assertEqual(member.email, "admin")

    def test_create_user(self):
        member = Member.objects.create(**self.member_data)
        self.assertEqual(Member.objects.count(), 2)

        self.assertEqual(member.email, self.member_data['email'])
        self.assertEqual(member.phone, self.member_data['phone'])
        self.assertEqual(member.first_name, self.member_data['first_name'])
        self.assertEqual(member.last_name, self.member_data['last_name'])

        member2 = Member.objects.create(**self.member2_data)
        self.assertEqual(Member.objects.count(), 3)

        self.assertEqual(member2.email, self.member2_data['email'])
        self.assertEqual(member2.phone, self.member2_data['phone'])
        self.assertEqual(member2.first_name, self.member2_data['first_name'])
        self.assertEqual(member2.last_name, self.member2_data['last_name'])

    def test_email_uniqueness(self):
        member = Member.objects.create(**self.member_data)
        self.assertEqual(member.email, self.member_data['email'])
        self.assertEqual(Member.objects.count(), 2)

        member2_data = self.member2_data
        member2_data['email'] = self.member_data['email']
        with self.assertRaises(IntegrityError):
            Member.objects.create(**member2_data)

    def test_phone_uniqueness(self):
        member = Member.objects.create(**self.member_data)
        self.assertEqual(member.phone, self.member_data['phone'])

        member2_data = self.member2_data
        member2_data['phone'] = self.member_data['phone']
        with self.assertRaises(IntegrityError):
            Member.objects.create(**member2_data)

    def test_role_default_value(self):
        self.member_data.pop('role')
        member = Member.objects.create(**self.member_data)
        self.assertEqual(member.role, Member.RoleChoices.regular)


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
        response = self.client.post(self.url, data=self.member_data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse_lazy('members:list'))
        self.assertEqual(Member.objects.count(), 2)
        member = Member.objects.last()
        self.assertEqual(member.first_name, self.member_data['first_name'])
        self.assertEqual(member.last_name, self.member_data['last_name'])
        self.assertEqual(member.phone, self.member_data['phone'])
        self.assertEqual(member.role, self.member_data['role'])
        self.assertEqual(member.email, self.member_data['email'])

    def test_email_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member_data.pop('email')
        response = self.client.post(self.url, data=self.member_data)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_email_uniqueness(self):
        Member.objects.create(**self.member_data)
        self.assertEqual(Member.objects.count(), 2)

        self.member2_data['email'] = self.member_data['email']
        response = self.client.post(self.url, data=self.member2_data)
        self.assertContains(response, "User with this Email address already exists.", count=1)
        self.assertEqual(Member.objects.count(), 2)

    def test_phone_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member_data.pop('phone')
        response = self.client.post(self.url, data=self.member_data)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_phone_uniqueness(self):
        Member.objects.create(**self.member_data)
        self.assertEqual(Member.objects.count(), 2)

        self.member2_data['phone'] = self.member_data['phone']
        response = self.client.post(self.url, data=self.member2_data)
        self.assertContains(response, "User with this Phone already exists.", count=1)
        self.assertEqual(Member.objects.count(), 2)

    def test_role_required(self):
        self.assertEqual(Member.objects.count(), 1)
        self.member_data.pop('role')
        response = self.client.post(self.url, data=self.member_data)
        self.assertContains(response, "This field is required.", count=1)
        self.assertEqual(Member.objects.count(), 1)

    def test_nameless_user(self):
        pass


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
        member = Member.objects.create(**self.member_data)
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
