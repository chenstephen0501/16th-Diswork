from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from .forms import EventForm
from .models import Event
from django.http import JsonResponse
from django.views.generic import FormView, ListView


@method_decorator(login_required, name="dispatch")
class CalendarView(ListView):
    template_name = "events/calendar.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all()


class NewView(FormView):
    form_class = EventForm
    template_name = "events/new.html"
    success_url = "/events/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@require_POST
def create(req):
    form = EventForm(req.POST)
    if form.is_valid():
        form.save()
        return redirect("events:calendar")
    else:
        return JsonResponse({"errors": form.errors}, status=400)


def edit(req, id):
    event = get_object_or_404(Event, pk=id)
    if req.method == "POST":
        form = EventForm(req.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:calendar")
    else:
        form = EventForm(instance=event)
    return render(req, "events/edit.html", {"form": form})


def all_events(req):
    all_events = Event.objects.all()
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
    event = Event(summary=str(title), start_time=start, end_time=end)
    event.save()
    data = {}
    return JsonResponse(data)
