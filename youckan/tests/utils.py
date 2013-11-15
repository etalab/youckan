# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.utils.importlib import import_module

from youckan.models import User


try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:     # Python 2
    from urlparse import urlsplit, urlunsplit


TEST_PASSWORD = 'password'


class TestHelper(object):
    def create_user(self, email):
        user = User.objects.create_user(email, TEST_PASSWORD)
        return user

    def create_and_log_user(self, email):
        user = self.create_user(email)
        self.client.login(email=email, password=TEST_PASSWORD)
        return user

    def prepare_session(self):
        # http://code.djangoproject.com/ticket/10899
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        if not self.client.cookies.get(settings.SESSION_COOKIE_NAME):
            store = engine.SessionStore()
            store.save()
            self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        else:
            store = engine.SessionStore(self.client.cookies[settings.SESSION_COOKIE_NAME])
        self.session = store

    def assert_redirects_to(self, response, url_name, status_code=302,
                            target_status_code=200, host=None, msg_prefix='', *args, **kwargs):
        '''
        Assert that the response is a redirect to a resolved url and that the URL can be loaded.

        It differs from Django TestCase.assertRedirects on the following points:

        - Takes a resolable url name as parameter
        - Query params are not taken in account for URL comparison, only for status code retrieval.
        '''
        if msg_prefix:
            msg_prefix += ": "

        if hasattr(response, 'redirect_chain'):
            # The request was a followed redirect
            self.assertTrue(len(response.redirect_chain) > 0,
                msg_prefix + "Response didn't redirect as expected: Response"
                " code was %d (expected %d)" %
                    (response.status_code, status_code))

            self.assertEqual(response.redirect_chain[0][1], status_code,
                msg_prefix + "Initial response didn't redirect as expected:"
                " Response code was %d (expected %d)" %
                    (response.redirect_chain[0][1], status_code))

            url, status_code = response.redirect_chain[-1]

            self.assertEqual(response.status_code, target_status_code,
                msg_prefix + "Response didn't redirect as expected: Final"
                " Response code was %d (expected %d)" %
                    (response.status_code, target_status_code))

        else:
            # Not a followed redirect
            self.assertEqual(response.status_code, status_code,
                msg_prefix + "Response didn't redirect as expected: Response"
                " code was %d (expected %d)" %
                    (response.status_code, status_code))

            url = response['Location']
            scheme, netloc, path, query, fragment = urlsplit(url)
            url = urlunsplit((scheme, netloc, path, None, None))

            redirect_response = response.client.get(path, QueryDict(query))

            # Get the redirection page, using the same client that was used
            # to obtain the original response.
            self.assertEqual(redirect_response.status_code, target_status_code,
                msg_prefix + "Couldn't retrieve redirection page '%s':"
                " response code was %d (expected %d)" %
                    (path, redirect_response.status_code, target_status_code))

        path = reverse(url_name, *args, **kwargs)
        expected_url = urlunsplit(('http', host or 'testserver', path, None, None))

        self.assertEqual(url, expected_url,
            msg_prefix + "Response redirected to '%s', expected '%s'" %
                (url, expected_url))
