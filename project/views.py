from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "pages/index.html"

class PremiumView(TemplateView):
    template_name = "pages/premium.html"
