from http import HTTPStatus

from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse
from django_webtest import WebTestMixin

from members.models import Member


class MemberTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        self.client = Client()
        self.member1_data = {
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
        member = Member.objects.create(**self.member1_data)
        self.assertEqual(Member.objects.count(), 2)

        self.assertEqual(member.email, self.member1_data['email'])
        self.assertEqual(member.phone, self.member1_data['phone'])
        self.assertEqual(member.first_name, self.member1_data['first_name'])
        self.assertEqual(member.last_name, self.member1_data['last_name'])

        member2 = Member.objects.create(**self.member2_data)
        self.assertEqual(Member.objects.count(), 3)

        self.assertEqual(member2.email, self.member2_data['email'])
        self.assertEqual(member2.phone, self.member2_data['phone'])
        self.assertEqual(member2.first_name, self.member2_data['first_name'])
        self.assertEqual(member2.last_name, self.member2_data['last_name'])

    def test_email_uniqueness(self):
        member = Member.objects.create(**self.member1_data)
        self.assertEqual(member.email, self.member1_data['email'])
        self.assertEqual(Member.objects.count(), 2)

        member2_data = self.member2_data
        member2_data['email'] = self.member1_data['email']
        with self.assertRaises(IntegrityError):
            Member.objects.create(**member2_data)

    def test_phone_uniqueness(self):
        member = Member.objects.create(**self.member1_data)
        self.assertEqual(member.phone, self.member1_data['phone'])

        member2_data = self.member2_data
        member2_data['phone'] = self.member1_data['phone']
        with self.assertRaises(IntegrityError):
            Member.objects.create(**member2_data)

    def test_role_default_value(self):
        self.member1_data.pop('role')
        member = Member.objects.create(**self.member1_data)
        self.assertEqual(member.role, Member.RoleChoices.regular)

    def test_is_admin(self):
        member1 = Member.objects.create(**self.member1_data)
        member2 = Member.objects.create(**self.member2_data)

        self.assertFalse(member1.is_admin)
        self.assertTrue(member2.is_admin)


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


class UpdateMemberViewTest(WebTestMixin, MemberTestCase):

    def setUp(self):
        super().setUp()
        self.member1 = Member.objects.create(**self.member1_data)
        self.member2 = Member.objects.create(**self.member2_data)

    def test_get_edit_member_page(self):
        response = self.client.get(reverse('members:edit', args=[self.member1.id]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Edit Member")
        member = response.context_data['object']
        self.assertEqual(member, self.member1)

        form = self.app.get(reverse('members:edit', args=[self.member1.id])).forms[0]
        self.assertEqual(form['first_name'].value, self.member1.first_name)
        self.assertEqual(form['last_name'].value, self.member1.last_name)
        self.assertEqual(form['phone'].value, self.member1.phone)
        self.assertEqual(form['email'].value, self.member1.email)
        self.assertEqual(form['role'].value, self.member1.role)

    def test_update_email(self):
        self.member1_data['email'] = "newEmail@gmail.com"
        response = self.client.post(reverse('members:edit', args=[self.member1.id]), data=self.member1_data,
                                    follow=True)
        self.assertRedirects(response, reverse_lazy('members:list'))
        self.assert_new_member(**self.member1_data)

    def test_update_phone(self):
        self.member1_data['phone'] = "333-444-5566"
        response = self.client.post(reverse('members:edit', args=[self.member1.id]), data=self.member1_data)
        self.assertRedirects(response, reverse_lazy('members:list'))
        self.assert_new_member(**self.member1_data)

    def test_update_first_and_last_name(self):
        self.member1_data.update({'first_name': "anderson", 'last_name': "tamson"})
        response = self.client.post(reverse('members:edit', args=[self.member1.id]),
                                    data=self.member1_data)
        self.assertRedirects(response, reverse_lazy('members:list'))
        self.assert_new_member(**self.member1_data)

    def assert_new_member(self, **kwargs):
        member = Member.objects.get(pk=self.member1.id)
        self.assertEqual(member.phone, kwargs['phone'])
        self.assertEqual(member.first_name, kwargs['first_name'])
        self.assertEqual(member.last_name, kwargs['last_name'])
        self.assertEqual(member.email, kwargs['email'])
        self.assertEqual(member.role, kwargs['role'])


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
