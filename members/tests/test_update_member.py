from http import HTTPStatus

from django.urls import reverse_lazy, reverse
from django_webtest import WebTestMixin

from members.models import Member
from members.tests.test_member_base import MemberTestCase


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
