from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "pages/index.html"

class PremiumView(TemplateView):
    template_name = "pages/premium.html"

def custom_page_not_found_view(request, exception):
    return render(request, "shared/404.html", {}, status=404)