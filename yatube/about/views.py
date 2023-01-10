from django.views.generic.base import TemplateView

# Create your views here.


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'


class EasterEggs(TemplateView):
    template_name = 'about/eastereggs.html'
