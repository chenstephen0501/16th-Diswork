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
    return render(
        request,
        "pages/index.html",
        {"member_status": member_status, "member": member_log},
    )


from news.models import News


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_items"] = News.objects.all().order_by("-created_at")[:10]
        return context


class AboutUsView(TemplateView):
    template_name = "pages/aboutus.html"
