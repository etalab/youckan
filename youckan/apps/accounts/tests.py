# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from youckan.tests.utils import TestHelper
from youckan.apps.accounts.widgets import ProfileWidget


class UserListTest(TestHelper, TestCase):
    def setUp(self):
        self.user = self.create_and_log_user('me@youckan.test')

    def test_render(self):
        for i in range(5):
            self.create_user('user-{0}@youckan.test'.format(i))

        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)


class FakeProfileWidget(ProfileWidget):
    name = 'Fake'
    template_name = 'accounts/widgets/fake.html'

    def fill_context(self, context):
        context['fake'] = 'Fake'


@override_settings(PROFILE_WIDGETS=['youckan.apps.accounts.tests.FakeProfileWidget'])
class UserProfileTest(TestHelper, TestCase):
    def test_render(self):
        user = self.create_user('user@youckan.test')

        response = self.client.get(reverse('profile', kwargs={'slug': user.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/widgets/fake.html')
        self.assertIn('fake', response.context)
        self.assertEqual('Fake', response.context['fake'])
