# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pkg_resources

from collections import OrderedDict
from optparse import make_option
from os.path import exists

from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str
from django.utils.six.moves import input


SECRET_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

OPTIONS = {
    'ini': {
        'filename': 'youckan.ini',
        'names': (
            'hostname',
            'logs',
            'domain',
        )
    },
    'nginx': {
        'filename': 'nginx.conf',
        'names': (
            'hostname',
            'logs',
        )
    },
    'apache': {
        'filename': 'apache.conf',
        'names': (
            'hostname',
            'logs',
        )
    },
    'uwsgi': {
        'filename': 'uwsgi.ini',
        'names': (
            'hostname',
            'logs',
        )
    },
    'wsgi': {
        'filename': 'youckan.wsgi',
        'names': []
    },
}

QUESTIONS = OrderedDict({
    'hostname': ('Public hostname', 'www.youckan.com'),
    'domain': ('Domain', 'youckan.com'),
    'logs': ('Log directory', '/var/log/youckan'),
})


class Command(BaseCommand):
    help = 'Generate a sample configuration file'
    option_list = BaseCommand.option_list + (
        make_option('--ini',
            action='store_true',
            dest='ini',
            default=False,
            help='Create a youckan.ini file'
        ),
        make_option('--nginx',
            action='store_true',
            dest='nginx',
            default=True,
            help='Create a nginx.conf file'
        ),
        make_option('--apache',
            action='store_true',
            dest='apache',
            default=True,
            help='Create a apache.conf file'
        ),
        make_option('--uwsgi',
            action='store_true',
            dest='uwsgi',
            default=True,
            help='Create a uwsgi.ini file'
        ),
        make_option('--wsgi',
            action='store_true',
            dest='wsgi',
            default=True,
            help='Create a youckan.wsgi file'
        ),
        make_option('--home',
            dest='home',
            default=os.getcwd(),
            help='Specify the YOUCKAN_HOME used in template (defaults to current working directory)'
        ),
    )

    def handle(self, *args, **options):
        names = []

        for option in OPTIONS.keys():
            if option in options:
                filename = OPTIONS[option]['filename']
                if exists(filename):
                    raise CommandError('{0} alredy exists'.format(filename))
                names.extend(OPTIONS[option]['names'])

        params = {
            'home': options['home'],
            'secret': get_random_string(50, SECRET_CHARS),
        }
        params.update(self.ask_questions(names))

        for option in OPTIONS.keys():
            if option in options:
                filename = OPTIONS[option]['filename']
                template = pkg_resources.resource_string('youckan', 'templates/config/{0}'.format(filename))
                with open(filename, 'wb') as out:
                    self.stdout.write('Creating {0}'.format(filename))
                    out.write(template.format(**params))

    def ask_questions(self, names):
        params = {}
        for name in QUESTIONS.keys():
            if name in names:
                question, default = QUESTIONS[name]
                response = input(force_str('{0} [{1}]: '.format(question, default)))
                params[name] = response or default
        return params
