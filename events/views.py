from django.shortcuts import render, redirect, get_object_or_404
from .utils import get_calendar_events
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def calendar_events(req):
    events = get_calendar_events()  # 從 Google Calendar API 獲取資料
    return render(req, "events/calendar.html", {"events": events})


# 自己新增活動的頁面
class NewView(FormView):
    form_class = myEventForm
    template_name = "events/new.html"


@require_POST
def create_my_event(req):
    form = myEventForm(req.POST)
    if form.is_valid():
        form.save()
        messages.success(req, "新增成功")
    return redirect("events:calendar")


# 編輯自己新增的活動
def edit(req, id):
    myEvents = get_object_or_404(myEvent, pk=id)
    return render(req, "events/edit.html", {"myEvents": myEvents})


# 自己新增的活動出現在日曆中
def my_event_calendar(req):
    myEvents = myEvent.objects.all()
    return render(req, "events/calendar.html", {"myEvents": myEvents})


# def myEvents(req):
#     myEvents = myEvent.objects.all()
#     out = []
#     for myevent in myEvents:
#         out.append(
#             {
#                 "title": myevent.summary,
#                 "id": myevent.id,
#                 "start": myevent.start_time.strftime("%m/%d/%y, %H,%M,%S"),
#                 "end": myevent.end_time.strftime("%m/%d/%y, %H,%M,%S"),
#                 "description": myevent.description,
#             }
#         )
#     return JsonResponse({"events": out}, safe=False)


# def add_event(req):
#     start = req.GET.get("start", None)
#     end = req.GET.get("end", None)
#     title = req.GET.get("title", None)
#     event = myEvents(name=str(title), start=start, end=end)
#     event.save()
#     data = {}
#     return JsonResponse(data)
