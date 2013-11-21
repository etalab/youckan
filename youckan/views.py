# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext, loader

JSON_CONTENT_TYPE = 'application/json'


class FormsetsMixin(object):

    formsets = {}
    formsets_initial = {}

    def get_context_data(self, **kwargs):
            context = super(FormsetsMixin, self).get_context_data(**kwargs)
            context['formsets'] = self.get_formsets()
            return context

    def get_formset_kwargs(self, formset):
        kwargs = self.get_form_kwargs()
        kwargs['initial'] = self.formsets_initial.get(formset, {}).copy()
        return kwargs

    def get_formsets(self):
        return dict((
            (name, clazz(**self.get_formset_kwargs(name)))
            for name, clazz in self.formsets.items()
        ))

    def form_valid(self, form):
        formsets = self.get_formsets()

        if not all((fs.is_valid() for fs in formsets.values())):
            return self.form_invalid(form)

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in formsets.items():
            formset_save = getattr(self, 'formset_{0}_valid'.format(name), formset.save)
            formset_save(formset)

        return HttpResponseRedirect(self.get_success_url())


def expect_json(request):
    '''Return True if the request expect JSON as response'''
    if request.is_ajax():
        return True
    elif request.META.get('CONTENT_TYPE') == JSON_CONTENT_TYPE:
        return True
    elif 'HTTP_ACCEPT' not in request.META:
        return False
    accepted = [accept.split(';')[0] for accept in request.META['HTTP_ACCEPT'].split(',')]
    return JSON_CONTENT_TYPE in accepted and (
        'text/html' not in accepted or accepted.index(JSON_CONTENT_TYPE) < accepted.index('text/html')
    )


def server_error(request, template_name='500.html'):
    '''A 500 server error handler with RequestContext.'''
    if expect_json(request):
        content = json.dumps({
            'error': 'server error (500)',
        })
        return HttpResponseServerError(content, content_type=JSON_CONTENT_TYPE)
    else:
        template = loader.get_template(template_name)
        context = RequestContext(request, {})
        return HttpResponseServerError(template.render(context))
