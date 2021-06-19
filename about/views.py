from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about_author.html'


class AboutSpecView(TemplateView):
    template_name = 'about_spec.html'
