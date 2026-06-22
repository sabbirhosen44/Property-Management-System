from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "property_app/home.html"
