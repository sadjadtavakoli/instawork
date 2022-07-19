from django.db import IntegrityError
from django.test import TestCase, Client

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
