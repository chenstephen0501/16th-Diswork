from django.shortcuts import render
from .utils import get_calendar_events


def calendar_events(request):
    print(request)
    events = get_calendar_events()  # 從 Google Calendar API 獲取資料
    return render(request, "events/calendar.html", {"events": events})
