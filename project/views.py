from django.shortcuts import render
from django.views.generic import TemplateView
from members.models import Member


def index(request):
    member_log = request.user
    if request.user.is_authenticated:
        try:
            member = Member.objects.get(username=request.user.username)
            member_status = member.member_status == "1"
        except Member.DoesNotExist:
            member_status = False
    else:
        member_status = False
    return render(request, "pages/index.html", {"member_status": member_status, "member":member_log})

class PremiumView(TemplateView):
    template_name = "pages/premium.html"
