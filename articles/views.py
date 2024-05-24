from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, FormView, DetailView, DeleteView
from django.contrib import messages
from .models import Article
from members.models import Member
from .forms import ArticleForm

# Create your views here.
class ArticleIndexView(ListView):
    model = Article
    template_name = "articles/index.html"

class NewView(FormView):
    def get(self, request):
        form = ArticleForm()
        return render(request, "articles/new.html", {"form": form})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = self.request.user
            article.save()
            return redirect("articles:index")
        return render(request, "articles/new.html", {"form": form})

class ShowView(DetailView):
    model = Article
    
    def post(self, request, pk):
        article = self.get_object()
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            messages.success(request, "新增成功")
        return redirect("articles:show", pk=article.id)


@require_POST
def create(request):
    form = ArticleForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "文章新增成功")
    return redirect("articles:index")

def edit(request, id):
    article = get_object_or_404(Article, pk = id)
    form = ArticleForm(instance=article)
    return render(request, "articles/edit.html", {"article": article, "form": form})


class DeleteView(DeleteView):
    model = Article

    def get_success_url(self):
        messages.success(self.request, "已刪除")
        return reverse("articles:index")
