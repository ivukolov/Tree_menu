from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'menu/index.html'

class HomePageTestView(TemplateView):
    template_name = 'menu/index.html'

