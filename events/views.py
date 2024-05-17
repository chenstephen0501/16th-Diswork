from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_calendar_events
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from .forms import myEventForm
from .models import my_event
from django.http import JsonResponse
from django.views.generic import FormView
from .forms import myEventForm


@login_required
def calendar_events(req):
    google_events = get_calendar_events()  # 從 Google Calendar API 獲取資料
    return render(req, "events/calendar.html", {"google_events": google_events})


# 新增活動的頁面
class NewView(FormView):
    form_class = myEventForm
    template_name = "events/new.html"
    success_url = "/events/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# @require_POST
def create_my_event(req):
    form = myEventForm(req.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"message": "Event created successfully"}, status=201)
    else:
        return JsonResponse({"errors": form.errors}, status=400)


# 編輯自己新增的活動
def edit(req, id):
    event = get_object_or_404(my_event, pk=id)
    if req.method == "POST":
        form = myEventForm(req.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:calendar")
    else:
        form = myEventForm(instance=event)
    return render(req, "events/edit.html", {"form": form})


# 自己新增的活動出現在日曆中
def my_event_calendar(req):
    my_events = my_event.objects.all()
    return render(req, "events/calendar.html", {"my_events": my_events})


def all_events(req):
    all_events = my_event.objects.all()
    out = []
    for event in all_events:
        start_time = (
            event.start_time.strftime("%Y-%m-%dT%H:%M:%S") if event.start_time else None
        )
        end_time = (
            event.end_time.strftime("%Y-%m-%dT%H:%M:%S") if event.end_time else None
        )
        out.append(
            {
                "title": event.summary,
                "id": event.id,
                "start": start_time,
                "end": end_time,
                "description": event.description,
                "url": "",
            }
        )
    return JsonResponse(out, safe=False)


def add_event(req):
    start = req.POST.get("start", None)
    end = req.POST.get("end", None)
    title = req.POST.get("title", None)
    event = my_event(summary=str(title), start_time=start, end_time=end)
    event.save()
    data = {}
    return JsonResponse(data)
