from django.shortcuts import redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from django.views.generic import ListView, FormView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from members.models import Member

@method_decorator(login_required, name="dispatch")
class BoardIndexView(ListView):
    model = Category
    template_name = "boards/board_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword", "").strip()
        return queryset.filter(title__icontains=keyword)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                member = Member.objects.get(username=self.request.user.username)
                context["member_status"] = member.member_status
            except Member.DoesNotExist:
                context["member_status"] = "0"
        else:
            context["member_status"] = "0"
        return context

@method_decorator(login_required, name="dispatch")
class BoardDetailView(DetailView):
    model = Category
    template_name = "boards/board_detail.html"


@method_decorator(login_required, name="dispatch")
class BoardNewView(FormView):
    form_class = CategoryForm
    template_name = "boards/new.html"


@login_required
@require_POST
def create(req):
    form = CategoryForm(req.POST, req.FILES)
    if form.is_valid():
        category = form.save(commit=False)
        category.member_id = req.user.id
        category.save()
        messages.success(req, "新增成功！")
    return redirect("boards:list")


@method_decorator(login_required, name="dispatch")
class BoardUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "boards/edit.html"

    def get_success_url(self):
        return reverse_lazy("boards:list")


@method_decorator(login_required, name="dispatch")
class BoardDeleteView(DeleteView):
    model = Category

    def get_success_url(self):
        messages.success(self.request, "已刪除")
        return reverse_lazy("boards:list")
