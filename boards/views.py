from django.shortcuts import redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from django.views.generic import ListView, FormView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class BoardIndexView(ListView):
    model = Category
    template_name = "boards/board_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword", "").strip()

        return queryset.filter(title__icontains=keyword)


class BoardDetailView(DetailView):
    model = Category
    template_name = "boards/board_detail.html"


class BoardNewView(FormView):
    form_class = CategoryForm
    template_name = "boards/new.html"


@require_POST
def create(req):
    form = CategoryForm(req.POST)
    if form.is_valid():
        form.save()
        messages.success(req, "新增成功！")
    return redirect("boards:list")


@method_decorator(login_required, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "boards/edit.html"

    def get_success_url(self):
        return reverse_lazy("boards:detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Category, pk=pk)


@method_decorator(login_required, name="dispatch")
class BoardDeleteView(DeleteView):
    model = Category

    def get_success_url(self):
        messages.success(self.request, "已刪除")
        return reverse_lazy("boards:list")
