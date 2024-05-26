from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import FormView
from .forms import EventForm
from .models import Event
from django.http import JsonResponse
from django.views.generic import FormView, ListView, UpdateView, DeleteView


@method_decorator(login_required, name="dispatch")
class CalendarView(ListView):
    template_name = "events/calendar.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all()


class EventListView(ListView):
    model = Event
    template_name = "events/event_detail.html"


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


@method_decorator(login_required, name="dispatch")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/edit.html"

    def get_success_url(self):
        return reverse_lazy("events:list")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Event, pk=pk)


class EventDeleteView(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse("events:list")


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
