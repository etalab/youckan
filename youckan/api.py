# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer, FileField, Field

from oauth2_provider.ext.rest_framework import permissions as oauth_permissions

from youckan.avatar import get_avatar_url
from youckan.models import User, UserProfile


class IsAuthenticatedOrTokenHasScope(oauth_permissions.TokenHasScope):
    '''
    Allows access only to authenticated users or to tokens with a specified scope.
    '''

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return True
        return super(IsAuthenticatedOrTokenHasScope, self).has_permission(request, view)


class HyperlinkedFileField(FileField):
    '''Render a FileField as an absolute url'''
    def to_native(self, value):
        request = self.context.get('request', None)
        return request.build_absolute_uri(value.url) if value else None


class AvatarField(HyperlinkedFileField):
    def field_to_native(self, obj, field_name):
        value = super(AvatarField, self).field_to_native(obj, field_name)
        return value if value else get_avatar_url(obj.user)


class UserProfileSerializer(ModelSerializer):
    avatar = AvatarField()

    class Meta:
        model = UserProfile
        fields = ('avatar', 'city', 'about', 'website')


class UserSerializer(ModelSerializer):
    fullname = Field('full_name')
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'email',
            'fullname',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'date_joined',
            'slug',
            'profile'
        )


class ProfileAPI(RetrieveAPIView):
    # model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['profile']

    def get_object(self):
        return self.request.user


class UserListAPIView(ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrTokenHasScope]
    required_scopes = ['read']
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name', 'slug')


urlpatterns = patterns('',
    url(r'^me/$', ProfileAPI.as_view(), name='api-my-profile'),
    url(r'^users/$', UserListAPIView.as_view(), name='api-users'),
)
