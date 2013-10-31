# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer, FileField
from rest_framework import permissions

from oauth2_provider.ext.rest_framework import TokenHasScope

from youckan.models import User, UserProfile


class HyperlinkedFileField(FileField):
    '''Render a FileField as an absolute url'''
    def to_native(self, value):
        request = self.context.get('request', None)
        return request.build_absolute_uri(value.url) if value else None


class UserProfileSerializer(ModelSerializer):
    avatar = HyperlinkedFileField()

    class Meta:
        model = UserProfile
        fields = ('avatar', 'city', 'about', 'website')


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_superuser', 'is_active', 'date_joined', 'slug', 'profile')


class ProfileAPI(RetrieveAPIView):
    # model = User
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['profile']

    def get_object(self):
        return self.request.user


urlpatterns = patterns('',
    url(r'^profile$', ProfileAPI.as_view(), name='api-profile'),
)
