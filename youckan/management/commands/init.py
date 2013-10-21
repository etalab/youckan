# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells YouCKAN to NOT prompt the user for input of any kind.'),
    )
    help = 'Initialize database and static assets'

    def handle(self, *args, **options):
        call_command('syncdb', **options)
        call_command('migrate', **options)
        call_command('collectstatic', **options)
