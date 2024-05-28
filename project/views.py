from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "pages/index.html"

class PremiumView(TemplateView):
    template_name = "pages/premium.html"
