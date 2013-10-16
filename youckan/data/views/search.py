from django.views.generic import TemplateView


class SearchView(TemplateView):
    template_name = 'search.html'
