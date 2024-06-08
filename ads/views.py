from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Ads
from .forms import AdsForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class AdsListView(ListView):
    model = Ads
    template_name = "ads/ad_list.html"
    context_object_name = "ads"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AdsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = AdsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("ads:list")

@method_decorator(login_required, name="dispatch")
class AdsCreateView(CreateView):
    model = Ads
    form_class = AdsForm
    template_name = "ads/ad_list.html"
    
    def get_success_url(self):
        return reverse_lazy("ads:list")

@method_decorator(login_required, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ads
    form_class = AdsForm
    template_name = "ads/edit.html"
    
    def get_success_url(self):
        return reverse_lazy("ads:list")

@method_decorator(login_required, name="dispatch")
class AdsDeleteView(DeleteView):
    model = Ads
    template_name = "ads/delete.html"
    
    def get_success_url(self):
        return reverse("ads:list")