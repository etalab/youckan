# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six
from djangojs.context_serializer import ContextSerializer


class SocialAuthContextMixin(object):
    '''Handle django_social_auth context specifics'''
    def process_backends(self, backends, data):
        """ Just force backends's LazyDict to be converted to a dict for the
            JSON serialization to work properly. """

        data['backends'] = dict(six.iteritems(backends))


class WeckanContextSerializer(SocialAuthContextMixin, ContextSerializer):
    '''Already packed django_social_auth ContextSerializer'''
    pass
