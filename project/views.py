from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    member = request.user
    return render(request, "pages/index.html", {"member": member})


class PremiumView(TemplateView):
    template_name = "pages/premium.html"
