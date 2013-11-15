# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pkg_resources

import httpretty

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from social.apps.django_app.default.models import UserSocialAuth
from social.backends.google import GoogleOAuth2

from youckan.models import User
from youckan.tests.utils import TestHelper
from youckan.apps.sso import pipeline

from factory.django import DjangoModelFactory


MAIL = 'me@youckan.test'
AVATAR_URL = 'http://test/avatar.jpg'


class SocialUserFactory(DjangoModelFactory):
    FACTORY_FOR = UserSocialAuth


class AuthPipelineTest(TestHelper, TestCase):
    def setUp(self):
        self.prepare_session()

    def test_register_no_social(self):
        '''Should handle registeration without social provider'''
        response = self.client.get(reverse('social:complete', args=['no-social']))
        self.assert_redirects_to(response, 'register')

    @httpretty.activate
    def test_register_google(self):
        '''Should handle registeration from Google'''
        self.mock_google()
        state = 'aaaaa'
        self.session['google-oauth2_state'] = state
        self.session.save()
        response = self.client.get(reverse('social:complete', args=['google-oauth2']), {'code': 'code', 'state': state})
        self.assert_redirects_to(response, 'register')
        self.assertEqual(self.get_from_pipeline('avatar_url'), AVATAR_URL)

    def test_register_linkedin(self):
        '''Should handle registeration from Linkedin'''

    def test_register_twitter(self):
        '''Should handle registeration from Twitter'''

    @httpretty.activate
    def test_register_social_exists(self):
        '''Should not let already registered social accounts to register (or login)'''
        user = self.create_user('coucou@c-encore-moi.fr')
        SocialUserFactory(uid=MAIL, provider=GoogleOAuth2.name, user=user)

        self.mock_google()
        response = self.client.get(reverse('social:complete', args=['google-oauth2']), {'code': 'code'})
        self.assert_redirects_to(response, 'login')

    def test_register_discard_avatar(self):
        '''Should discard avatar if chosen'''
        pipeline_index = settings.SOCIAL_AUTH_PIPELINE.index('youckan.apps.sso.pipeline.register_form')
        self.mock_partial_pipeline(pipeline_index)

        response = self.client.post(reverse('register'), follow=True, data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': MAIL,
            'raw_password': 'password',
            'password_confirm': 'password',
            'use_avatar': False,
        })

        self.assert_redirects_to(response, 'register-mail')
        self.assertIsNone(self.get_from_pipeline('avatar_url'))

    def test_register_keep_avatar(self):
        '''Should keep avatar if chosen'''
        pipeline_index = settings.SOCIAL_AUTH_PIPELINE.index('youckan.apps.sso.pipeline.register_form')
        self.mock_partial_pipeline(pipeline_index, avatar_url=AVATAR_URL)

        response = self.client.post(reverse('register'), follow=True, data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': MAIL,
            'raw_password': 'password',
            'password_confirm': 'password',
            'use_avatar': True,
        })

        self.assert_redirects_to(response, 'register-mail')
        self.assertEqual(self.get_from_pipeline('avatar_url'), AVATAR_URL)

    @httpretty.activate
    def test_fetch_avatar(self):
        '''Should keep avatar if chosen'''
        user = self.create_user(MAIL)
        self.mock_avatar_download()

        pipeline.fetch_avatar(None, None, user, AVATAR_URL)
        self.assertIsNotNone(user.profile.avatar.url)

    def mock_partial_pipeline(self, index=0, backend='no-social', *args, **kwargs):
        self.session['siteid'] = 'fake'
        self.session['partial_pipeline'] = {
            'next': index,
            'backend': backend,
            'args': args,
            'kwargs': dict(
                response=kwargs.pop('response', {}),
                details=kwargs.pop('details', {}),
                **kwargs
            )
        }
        self.session.save()

    def mock_avatar_download(self, avatar_url=AVATAR_URL):
        httpretty.register_uri(httpretty.GET, avatar_url,
            body=pkg_resources.resource_stream('youckan', 'static/images/certified-stamp.png'),
            content_type='image/png',
            streaming=True,
        )

    def get_from_pipeline(self, key, default=None):
        '''Get a value from session persisted pipeline'''
        return self.client.session.get('partial_pipeline', {}).get('kwargs', {}).get(key, default)

    def mock_google(self, email=MAIL, avatar_url=AVATAR_URL):
        '''Mock Google token and profile retrievals'''
        userinfos = {
            'id': '1234',
            'email': email,
            'verified_email': True,
            'name': 'Coucou CMoi',
            'given_name': 'Coucou',
            'family_name': 'CMoi',
            'link': 'https://test/me',
            'picture': avatar_url,
            'gender': 'male',
            'birthday': '0000-10-05',
            'locale': 'en',
        }
        token = {
            'access_token': 'access-token',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': 'refresh-token',
        }
        # Mock token
        httpretty.register_uri(httpretty.POST, GoogleOAuth2.ACCESS_TOKEN_URL,
            body=json.dumps(token),
            content_type='application/json'
        )
        # Mock user details
        httpretty.register_uri(httpretty.GET, 'https://www.googleapis.com/oauth2/v1/userinfo',
            body=json.dumps(userinfos),
            content_type='application/json'
        )
