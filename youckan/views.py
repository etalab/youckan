# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect


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
