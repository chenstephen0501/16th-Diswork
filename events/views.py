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
from boards.models import Category


@method_decorator(login_required, name="dispatch")
class CalendarView(ListView):
    template_name = "events/calendar.html"
    context_object_name = "events"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Event.objects.filter(category_id=category_id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, id=category_id)
        
        return context

    
@method_decorator(login_required, name="dispatch")
class EventListView(ListView):
    model = Event
    template_name = "events/event_detail.html"

    def get_queryset(self):
        return Event.objects.filter(category_id= self.kwargs.get("category_id"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        context["category"] = get_object_or_404(Category, id=category_id)

        return context

@method_decorator(login_required, name="dispatch")
class NewView(FormView):
    form_class = EventForm
    template_name = "events/new.html"

    def get_success_url(self):
        category_id = self.kwargs["category_id"]
        return reverse_lazy("events:calender", kwargs={"category_id": category_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        context["category"] = get_object_or_404(Category, id=category_id)
        
        return context

    def form_valid(self, form):
        form.instance.category_id = self.kwargs["category_id"]
        form.save()
        return super().form_valid(form)


@login_required
@require_POST
def create(req, category_id):
    form = EventForm(req.POST)

    if form.is_valid():
        event = form.save(commit=False)
        event.category_id = category_id
        event.save()
        return redirect(reverse("events:calendar", kwargs={"category_id": category_id}))
    else:
        return JsonResponse({"errors": form.errors}, status=400)


@method_decorator(login_required, name="dispatch")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/edit.html"

    def form_valid(self, form):
        form.instance.category_id = self.kwargs["category_id"]
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, id=self.kwargs.get("category_id"))
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Event, pk=pk)

    def get_success_url(self):
        print(self)
        category_id = self.kwargs["category_id"]
        return reverse_lazy("events:calendar", kwargs={"category_id": category_id})

class EventDeleteView(DeleteView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, id=self.kwargs["category_id"])
        return context

    def get_success_url(self):
        category_id = self.kwargs['category_id']
        return reverse_lazy("events:calendar", kwargs={"category_id": category_id})

@login_required
def all_events(req, category_id):
    all_events = Event.objects.filter(category_id=category_id)
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


@login_required
def add_event(req):
    start = req.POST.get("start", None)
    end = req.POST.get("end", None)
    title = req.POST.get("title", None)
    event = Event(summary=str(title), start_time=start, end_time=end)
    event.save()
    data = {}
    return JsonResponse(data)
